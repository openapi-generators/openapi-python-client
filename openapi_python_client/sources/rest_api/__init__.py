"""Generic API Source"""

import copy
from typing import (
    Type,
    Any,
    Dict,
    Tuple,
    List,
    Optional,
    Union,
    Generator,
    cast,
)
import graphlib  # type: ignore[import-untyped]

import dlt
from dlt.common.validation import validate_dict
from dlt.extract.incremental import Incremental
from dlt.extract.source import DltResource, DltSource
from dlt.common import logger, jsonpath
from dlt.common.utils import update_dict_nested
from dlt.common.typing import TSecretStrValue

from .auth import BearerTokenAuth, AuthConfigBase
from .client import RESTClient
from .detector import single_entity_path
from .paginators import (
    BasePaginator,
    HeaderLinkPaginator,
    JSONResponsePaginator,
    SinglePagePaginator,
    JSONResponseCursorPaginator,
)
from .typing import (
    AuthConfig,
    ClientConfig,
    IncrementalConfig,
    PaginatorType,
    ResolveConfig,
    ResolvedParam,
    Endpoint,
    EndpointResource,
    RESTAPIConfig,
    HTTPMethodBasic,
)


PAGINATOR_MAP: Dict[str, Type[BasePaginator]] = {
    "json_links": JSONResponsePaginator,
    "header_links": HeaderLinkPaginator,
    "auto": None,
    "single_page": SinglePagePaginator,
    "cursor": JSONResponseCursorPaginator,
}


def get_paginator_class(paginator_type: str) -> Type[BasePaginator]:
    try:
        return PAGINATOR_MAP[paginator_type]
    except KeyError:
        available_options = ", ".join(PAGINATOR_MAP.keys())
        raise ValueError(
            f"Invalid paginator: {paginator_type}. "
            f"Available options: {available_options}"
        )


def create_paginator(paginator_config: PaginatorType) -> Optional[BasePaginator]:
    if isinstance(paginator_config, BasePaginator):
        return paginator_config

    if isinstance(paginator_config, str):
        paginator_class = get_paginator_class(paginator_config)
        return paginator_class()

    if isinstance(paginator_config, dict):
        paginator_type = paginator_config.pop("type", "auto")
        paginator_class = get_paginator_class(paginator_type)
        return paginator_class(paginator_config)

    return None


def create_auth(
    auth_config: Optional[Union[AuthConfig, AuthConfigBase]],
) -> Optional[AuthConfigBase]:
    if isinstance(auth_config, AuthConfigBase):
        return auth_config
    return (
        BearerTokenAuth(cast(TSecretStrValue, auth_config.get("token")))
        if auth_config
        else None
    )


def make_client_config(config: RESTAPIConfig) -> ClientConfig:
    client_config = config.get("client", {})
    return ClientConfig(
        base_url=client_config.get("base_url"),
        auth=create_auth(client_config.get("auth")),
        paginator=create_paginator(client_config.get("paginator")),
    )


def setup_incremental_object(
    request_params: Dict[str, Any],
    incremental_config: Optional[IncrementalConfig] = None,
) -> Tuple[Optional[Incremental[Any]], Optional[str]]:
    for key, value in request_params.items():
        if isinstance(value, dlt.sources.incremental):
            return value, key
        if isinstance(value, dict):
            param_type = value.pop("type")
            if param_type == "incremental":
                return (
                    dlt.sources.incremental(**value),
                    key,
                )
    if incremental_config:
        param = incremental_config.pop("param")
        return dlt.sources.incremental(**incremental_config), param

    return None, None


def make_parent_key_name(resource_name: str, field_name: str) -> str:
    return f"_{resource_name}_{field_name}"


@dlt.source
def rest_api_source(config: RESTAPIConfig) -> List[DltResource]:
    """
    Creates and configures a REST API source for data extraction.

    Example:
        pokemon_source = rest_api_source({
            "client": {
                "base_url": "https://pokeapi.co/api/v2/",
                "paginator": "json_links",
            },
            "endpoints": {
                "pokemon": {
                    "params": {
                        "limit": 100, # Default page size is 20
                    },
                    "resource": {
                        "primary_key": "id",
                    }
                },
            },
        })
    """
    return rest_api_resources(config)


def rest_api_resources(config: RESTAPIConfig) -> List[DltResource]:
    """
    Creates and configures a REST API source for data extraction.

    Example:
        github_source = rest_api_resources_v3({
            "client": {
                "base_url": "https://api.github.com/repos/dlt-hub/dlt/",
                "auth": {
                    "token": dlt.secrets["token"],
                },
            },
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
                },
            ],
        })
    """

    validate_dict(RESTAPIConfig, config, path=".")

    client = RESTClient(**make_client_config(config))
    dependency_graph = graphlib.TopologicalSorter()
    endpoint_resource_map: Dict[str, EndpointResource] = {}
    resources = {}

    default_resource_config = config.get("resource_defaults", {})

    resource_list = config.get("resources")

    if resource_list is None:
        raise ValueError("No resources defined")

    # Create the dependency graph
    for resource_kwargs in resource_list:
        endpoint_resource = make_endpoint_resource(
            resource_kwargs, default_resource_config
        )

        resource_name = endpoint_resource["name"]

        resolved_params = find_resolved_params(
            cast(Endpoint, endpoint_resource["endpoint"])
        )

        if len(resolved_params) > 1:
            raise ValueError(
                f"Multiple resolved params for resource {resource_name}: {resolved_params}"
            )

        predecessors = set(x.resolve_config.resource_name for x in resolved_params)

        dependency_graph.add(resource_name, *predecessors)
        endpoint_resource["_resolved_param"] = (
            resolved_params[0] if resolved_params else None
        )

        if resource_name in endpoint_resource_map:
            raise ValueError(f"Resource {resource_name} has already been defined")

        endpoint_resource_map[resource_name] = endpoint_resource

    # Create the resources
    for resource_name in dependency_graph.static_order():
        endpoint_resource = endpoint_resource_map[resource_name]
        endpoint_config = endpoint_resource.pop("endpoint")
        request_params = endpoint_config.get("params", {})
        paginator = create_paginator(endpoint_config.get("paginator"))

        # TODO: Remove _resolved_param from endpoint_resource
        resolved_param: ResolvedParam = endpoint_resource.pop("_resolved_param", None)
        include_from_parent: List[str] = endpoint_resource.pop(
            "include_from_parent", []
        )
        if not resolved_param and include_from_parent:
            raise ValueError(
                f"Resource {resource_name} has include_from_parent but is not "
                "dependent on another resource"
            )

        incremental_object, incremental_param = setup_incremental_object(
            request_params, endpoint_resource.get("incremental")
        )

        response_actions = endpoint_config.get("response_actions")

        # try to guess if list of entities or just single entity is returned
        if single_entity_path(endpoint_config["path"]):
            data_selector = "$"
        else:
            data_selector = None

        if resolved_param is None:

            def paginate_resource(
                method: HTTPMethodBasic,
                path: str,
                params: Dict[str, Any],
                paginator: Optional[BasePaginator],
                data_selector: Optional[jsonpath.TJsonPath],
                response_actions: Optional[List[Dict[str, Any]]],
                incremental_object: Optional[Incremental[Any]] = incremental_object,
                incremental_param: str = incremental_param,
            ) -> Generator[Any, None, None]:
                if incremental_object:
                    params[incremental_param] = incremental_object.last_value

                yield from client.paginate(
                    method=method,
                    path=path,
                    params=params,
                    paginator=paginator,
                    data_selector=data_selector,
                    response_actions=response_actions,
                )

            resources[resource_name] = dlt.resource(
                paginate_resource, **endpoint_resource
            )(
                method=endpoint_config.get("method", "get"),
                path=endpoint_config.get("path"),
                params=request_params,
                paginator=paginator,
                data_selector=endpoint_config.get("data_selector") or data_selector,
                response_actions=response_actions,
            )

        else:
            predecessor = resources[resolved_param.resolve_config.resource_name]

            param_name = resolved_param.param_name
            request_params.pop(param_name, None)

            def paginate_dependent_resource(
                items: List[Dict[str, Any]],
                method: HTTPMethodBasic,
                path: str,
                params: Dict[str, Any],
                paginator: Optional[BasePaginator],
                data_selector: Optional[jsonpath.TJsonPath],
                response_actions: Optional[List[Dict[str, Any]]],
                param_name: str = param_name,
                field_path: str = resolved_param.resolve_config.field_path,
            ) -> Generator[Any, None, None]:
                items = items or []
                for item in items:
                    formatted_path = path.format(**{param_name: item[field_path]})
                    parent_resource_name = resolved_param.resolve_config.resource_name

                    parent_record = (
                        {
                            make_parent_key_name(parent_resource_name, key): item[key]
                            for key in include_from_parent
                        }
                        if include_from_parent
                        else None
                    )

                    for child_page in client.paginate(
                        method=method,
                        path=formatted_path,
                        params=params,
                        paginator=paginator,
                        data_selector=data_selector,
                        response_actions=response_actions,
                    ):
                        if parent_record:
                            for child_record in child_page:
                                child_record.update(parent_record)
                        yield child_page

            resources[resource_name] = dlt.resource(
                paginate_dependent_resource,
                data_from=predecessor,
                **endpoint_resource,
            )(
                method=endpoint_config.get("method", "get"),
                path=endpoint_config.get("path"),
                params=request_params,
                paginator=paginator,
                data_selector=endpoint_config.get("data_selector") or data_selector,
                response_actions=response_actions,
            )

    return list(resources.values())


def make_endpoint_resource(
    resource: Union[str, EndpointResource], default_config: EndpointResource
) -> EndpointResource:
    """
    Creates an EndpointResource object based on the provided resource
    definition and merges it with the default configuration.

    This function supports defining a resource in multiple formats:
    - As a string: The string is interpreted as both the resource name
        and its endpoint path.
    - As a dictionary: The dictionary must include `name` and `endpoint`
        keys. The `endpoint` can be a string representing the path,
        or a dictionary for more complex configurations. If the `endpoint`
        is missing the `path` key, the resource name is used as the `path`.
    """
    if isinstance(resource, str):
        resource = {"name": resource, "endpoint": {"path": resource}}
        return update_dict_nested(copy.deepcopy(default_config), resource)  # type: ignore[type-var]

    if "endpoint" in resource and isinstance(resource["endpoint"], str):
        resource["endpoint"] = {"path": resource["endpoint"]}

    if "name" not in resource:
        raise ValueError("Resource must have a name")

    if "path" not in resource["endpoint"]:
        resource["endpoint"]["path"] = resource["name"]  # type: ignore

    return update_dict_nested(copy.deepcopy(default_config), resource)  # type: ignore[type-var]


def make_resolved_param(
    key: str, value: Union[ResolveConfig, Dict[str, Any]]
) -> Optional[ResolvedParam]:
    if isinstance(value, ResolveConfig):
        return ResolvedParam(key, value)
    if isinstance(value, dict) and value.get("type") == "resolve":
        return ResolvedParam(
            key,
            ResolveConfig(resource_name=value["resource"], field_path=value["field"]),
        )
    return None


def find_resolved_params(endpoint_config: Endpoint) -> List[ResolvedParam]:
    """
    Find all resolved params in the endpoint configuration and return
    a list of ResolvedParam objects.

    Resolved params are either of type ResolveConfig or are dictionaries
    with a key "type" set to "resolve".
    """
    return [
        make_resolved_param(key, value)
        for key, value in endpoint_config.get("params", {}).items()
        if isinstance(value, ResolveConfig)
        or (isinstance(value, dict) and value.get("type") == "resolve")
    ]


def check_connection(
    source: DltSource,
    *resource_names: str,
) -> Tuple[bool, str]:
    try:
        list(source.with_resources(*resource_names).add_limit(1))
        return (True, "")
    except Exception as e:
        logger.error(f"Error checking connection: {e}")
        return (False, str(e))
