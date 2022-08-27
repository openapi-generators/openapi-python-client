import pytest
from pydantic import ValidationError

from openapi_python_client.schema import OpenAPI


@pytest.mark.parametrize(
    "version, valid", [("abc", False), ("1", False), ("2.0", False), ("3.0.0", True), ("3.1.0-b.3", False), (1, False)]
)
def test_validate_version(version, valid):
    data = {"openapi": version, "info": {"title": "test", "version": ""}, "paths": {}}
    if valid:
        OpenAPI.parse_obj(data)
    else:
        with pytest.raises(ValidationError):
            OpenAPI.parse_obj(data)


def test_parse_with_callback():
    data = {
        "openapi": "3.0.1",
        "info": {"title": "API with Callback", "version": ""},
        "paths": {
            "/create": {
                "post": {
                    "responses": {"200": {"description": "Success"}},
                    "callbacks": {"event": {"callback": {"post": {"responses": {"200": {"description": "Success"}}}}}},
                }
            }
        },
    }

    open_api = OpenAPI.parse_obj(data)
    create_endpoint = open_api.paths["/create"]
    assert "200" in create_endpoint.post.responses
    assert "200" in create_endpoint.post.callbacks["event"]["callback"].post.responses
