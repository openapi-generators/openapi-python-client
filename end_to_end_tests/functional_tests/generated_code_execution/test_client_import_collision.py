import asyncio
import json
from collections.abc import Iterator
from http import HTTPStatus
from typing import get_type_hints

import httpx
import pytest

from end_to_end_tests.generated_client import GeneratedClientContext, generate_client_from_inline_spec

ISSUE_SPEC = """
openapi: "3.0.3"
info:
  title: Minimal repro
  version: "1.0"
paths:
  /api/clients/{id}:
    patch:
      operationId: update_client
      tags:
        - client
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                name:
                  type: string
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Client"
components:
  schemas:
    Client:
      type: object
      properties:
        name:
          type: string
"""


@pytest.fixture(params=["Client", "AuthenticatedClient", "Response", "HTTPStatus", "Customer"])
def generated_client(request: pytest.FixtureRequest) -> Iterator[GeneratedClientContext]:
    # Client is the original issue document; Customer is a non-collision control.
    spec = ISSUE_SPEC.replace("Client", request.param)
    with generate_client_from_inline_spec(
        spec, base_module="minimal_repro_client", add_missing_sections=False
    ) as generated:
        yield generated


def test_endpoint_types_and_requests(generated_client: GeneratedClientContext) -> None:
    endpoint = generated_client.import_module(".api.client.update_client")
    transport = generated_client.import_module(".client")
    model = get_type_hints(endpoint._parse_response)["return"]
    models = generated_client.import_module(".models")
    response_type = generated_client.import_symbol(".types", "Response")
    body_type = generated_client.import_symbol(".models", "UpdateClientBody")
    package = generated_client.import_module("")

    # Compare with public exports, independently of endpoint import aliases.
    schema_model = next(
        getattr(models, name)
        for name in ("Client", "AuthenticatedClient", "Response", "HTTPStatus", "Customer")
        if hasattr(models, name)
    )
    assert model == schema_model | None
    assert package.Client is transport.Client
    assert package.AuthenticatedClient is transport.AuthenticatedClient
    assert schema_model is not transport.Client
    assert schema_model is not transport.AuthenticatedClient
    assert schema_model is not response_type

    for function_name in ("_parse_response", "_build_response", "sync", "sync_detailed", "asyncio", "asyncio_detailed"):
        hints = get_type_hints(getattr(endpoint, function_name))
        assert hints["client"] == transport.AuthenticatedClient | transport.Client
        detailed = function_name == "_build_response" or function_name.endswith("_detailed")
        assert hints["return"] == (response_type[schema_model] if detailed else schema_model | None)

    def handle_request(request: httpx.Request) -> httpx.Response:
        assert request.method == "PATCH"
        assert request.url.path == "/api/clients/one"
        assert json.loads(request.content) == {"name": "Ada"}
        return httpx.Response(200, json={"name": "Ada"})

    def check_result(result, detailed: bool) -> None:
        if detailed:
            assert type(result) is response_type
            assert result.status_code is HTTPStatus.OK
            result = result.parsed
        assert type(result) is schema_model
        assert result.name == "Ada"

    with httpx.Client(base_url="https://example.test", transport=httpx.MockTransport(handle_request)) as http_client:
        client = transport.Client(base_url="https://example.test").set_httpx_client(http_client)
        for operation in (endpoint.sync, endpoint.sync_detailed):
            check_result(
                operation("one", client=client, body=body_type(name="Ada")), operation is endpoint.sync_detailed
            )

    async def call_async() -> None:
        async with httpx.AsyncClient(
            base_url="https://example.test", transport=httpx.MockTransport(handle_request)
        ) as http_client:
            client = transport.AuthenticatedClient(
                base_url="https://example.test", token="token"
            ).set_async_httpx_client(http_client)
            for operation in (endpoint.asyncio, endpoint.asyncio_detailed):
                check_result(
                    await operation("one", client=client, body=body_type(name="Ada")),
                    operation is endpoint.asyncio_detailed,
                )

    asyncio.run(call_async())


def test_authenticated_endpoint_client_type() -> None:
    spec = (
        ISSUE_SPEC.replace("Client", "AuthenticatedClient")
        .replace("operationId: update_client", "operationId: update_client\n      security: [{bearer: []}]")
        .replace("components:", "components:\n  securitySchemes:\n    bearer:\n      type: http\n      scheme: bearer")
    )
    with generate_client_from_inline_spec(
        spec, base_module="minimal_repro_client", add_missing_sections=False
    ) as generated:
        endpoint = generated.import_module(".api.client.update_client")
        transport = generated.import_symbol(".client", "AuthenticatedClient")
        for function_name in ("sync", "sync_detailed", "asyncio", "asyncio_detailed"):
            assert get_type_hints(getattr(endpoint, function_name))["client"] is transport
