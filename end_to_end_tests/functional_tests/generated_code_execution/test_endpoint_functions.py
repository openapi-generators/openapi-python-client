"""Every generated endpoint module must expose a callable public API.

The fork generates exactly two functions per endpoint: the public ``request``, and
``_request_detailed`` for callers that need status and headers. ``request`` therefore has
to be generated unconditionally -- when it is skipped, the module's entire public surface
is empty and the endpoint cannot be called at all without reaching for an underscored
name.

The case that made this visible: a FastAPI route annotated ``-> None`` is described as a
200 with an empty schema, which the generator resolves to ``Any``.
"""

import asyncio
import inspect
from typing import Any

import httpx

from end_to_end_tests.functional_tests.helpers import (
    with_generated_client_fixture,
    with_generated_code_import,
    with_generated_code_imports,
)


def call(Client: Any, endpoint: Any, status_code: int = 200, json: Any = None, **kwargs: Any) -> Any:
    def handler(request: httpx.Request) -> httpx.Response:
        if json is None:
            return httpx.Response(status_code)
        return httpx.Response(status_code, json=json)

    client = Client(base_url="https://example.com")
    client.set_async_httpx_client(
        httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://example.com")
    )
    return asyncio.run(endpoint(client=client, **kwargs))


@with_generated_client_fixture(
    """
paths:
  "/typed":
    get:
      operationId: getTyped
      responses:
        "200":
          description: Success
          content:
            application/json:
              schema:
                type: object
                properties:
                  name: {type: string}
                required: ["name"]
  "/untyped":
    get:
      operationId: getUntyped
      responses:
        "200":
          description: Success
          content:
            application/json:
              schema: {}
  "/no-content":
    delete:
      operationId: deleteThing
      responses:
        "204":
          description: No Content
"""
)
@with_generated_code_imports(".client.Client")
@with_generated_code_import(".api.default.get_typed.request", alias="get_typed")
@with_generated_code_import(".api.default.get_untyped.request", alias="get_untyped")
@with_generated_code_import(".api.default.delete_thing.request", alias="delete_thing")
class TestPublicRequestFunction:
    def test_typed_response_is_parsed(self, Client, get_typed):
        assert call(Client, get_typed, json={"name": "x"}).name == "x"

    def test_untyped_response_still_callable(self, Client, get_untyped):
        """FastAPI's ``-> None``: a 200 whose schema is empty, so there is nothing to parse."""
        assert call(Client, get_untyped, json={"anything": 1}) is None

    def test_no_content_response_still_callable(self, Client, delete_thing):
        assert call(Client, delete_thing, status_code=204) is None

    def test_module_exposes_request_publicly(self, generated_client):
        for module_name in ("get_typed", "get_untyped", "delete_thing"):
            module = generated_client.import_module(f".api.default.{module_name}")
            public = [name for name in vars(module) if not name.startswith("_")]
            assert "request" in public, f"{module_name} has no public entry point; exports {public}"

    def test_unparsed_endpoints_are_annotated_none_not_any(self, generated_client):
        """`Any` would advertise a value that these endpoints never produce."""
        Response = generated_client.import_symbol(".types", "Response")
        for module_name in ("get_untyped", "delete_thing"):
            module = generated_client.import_module(f".api.default.{module_name}")
            assert inspect.signature(module.request).return_annotation is None
            assert inspect.signature(module._request_detailed).return_annotation == Response[None]

    def test_parsed_endpoint_keeps_its_response_type(self, generated_client):
        model = generated_client.import_symbol(".models", "GetTypedResponse200")
        module = generated_client.import_module(".api.default.get_typed")
        assert inspect.signature(module.request).return_annotation is model
