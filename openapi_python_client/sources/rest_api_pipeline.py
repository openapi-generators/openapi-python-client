import dlt
from rest_api import RESTAPIConfig, check_connection, rest_api_source


def load_github() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="rest_api_github_v3",
        destination='postgres',
        dataset_name="rest_api_data",
    )

    github_config: RESTAPIConfig = {
        "client": {
            "base_url": "https://api.github.com/repos/dlt-hub/dlt/",
            "auth": {
                "token": dlt.secrets["github_token"],
            },
        },
        # Default params for all resouces and their endpoints
        "resource_defaults": {
            "primary_key": "id",
            "write_disposition": "merge",
            "endpoint": {
                "params": {
                    "per_page": 100,
                },
            },
        },
        "resources": [
            # "pulls", <- This is both name and endpoint path
            # {
            #     "name": "pulls",
            #     "endpoint": "pulls",  # <- This is the endpoint path
            # }
            {
                "name": "issues",
                "endpoint": {
                    "path": "issues",
                    "params": {
                        "sort": "updated",
                        "direction": "desc",
                        "state": "open",
                        "since": {
                            "type": "incremental",
                            "cursor_path": "updated_at",
                            "initial_value": "2024-01-25T11:21:28Z",
                        },
                    },
                },
            },
            {
                "name": "issue_comments",
                "endpoint": {
                    "path": "issues/{issue_number}/comments",
                    "params": {
                        "issue_number": {
                            "type": "resolve",
                            "resource": "issues",
                            "field": "number",
                        }
                    },
                },
                "include_from_parent": ["id"],
            },
        ],
    }

    not_connecting_config: RESTAPIConfig = {
        **github_config,
        "client": {
            "base_url": "https://api.github.com/repos/dlt-hub/dlt/",
            "auth": {"token": "invalid token"},
        },
    }

    not_connecting_gh_source = rest_api_source(not_connecting_config)
    (can_connect, error_msg) = check_connection(not_connecting_gh_source, "issues")
    assert not can_connect, "A miracle happened. Token should be invalid"

    github_source = rest_api_source(github_config)

    load_info = pipeline.run(github_source)
    print(load_info)


def load_pokemon() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="rest_api_pokemon",
        destination='postgres',
        dataset_name="rest_api_data",
    )

    pokemon_source = rest_api_source(
        {
            "client": {
                "base_url": "https://pokeapi.co/api/v2/",
                # If you leave out the paginator, it will be inferred from the API:
                # paginator: "json_links",
            },
            "resource_defaults": {
                "endpoint": {
                    "params": {
                        "limit": 1000,
                    },
                },
            },
            "resources": [
                "pokemon",
                "berry",
                "location",
            ],
        }
    )

    def check_network_and_authentication() -> None:
        (can_connect, error_msg) = check_connection(
            pokemon_source,
            "not_existing_endpoint",
        )
        if not can_connect:
            pass  # do something with the error message

    check_network_and_authentication()

    load_info = pipeline.run(pokemon_source)
    print(load_info)


if __name__ == "__main__":
    load_github()
    load_pokemon()
