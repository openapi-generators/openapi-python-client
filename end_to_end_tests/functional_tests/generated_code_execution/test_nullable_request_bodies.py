import asyncio
import datetime
import inspect
import json
import subprocess
import sys
from typing import Any, get_args

import httpx
import pytest

from end_to_end_tests.functional_tests.helpers import with_generated_client_fixture


def _sync_request(
    endpoint: Any,
    Client: Any,
    *,
    body: Any = inspect.Parameter.empty,
) -> httpx.Request:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(204)

    with httpx.Client(base_url="https://example.test", transport=httpx.MockTransport(handler)) as httpx_client:
        client = Client(base_url="https://example.test").set_httpx_client(httpx_client)
        if body is inspect.Parameter.empty:
            endpoint.sync_detailed(client=client)
        else:
            endpoint.sync_detailed(client=client, body=body)

    assert len(requests) == 1
    return requests[0]


def _async_request(
    endpoint: Any,
    Client: Any,
    *,
    body: Any = inspect.Parameter.empty,
) -> httpx.Request:
    requests: list[httpx.Request] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(204)

    async def send() -> None:
        async with httpx.AsyncClient(
            base_url="https://example.test", transport=httpx.MockTransport(handler)
        ) as httpx_client:
            client = Client(base_url="https://example.test").set_async_httpx_client(httpx_client)
            if body is inspect.Parameter.empty:
                await endpoint.asyncio_detailed(client=client)
            else:
                await endpoint.asyncio_detailed(client=client, body=body)

    asyncio.run(send())
    assert len(requests) == 1
    return requests[0]


OPENAPI_30_SPEC = """
openapi: 3.0.3
info: {title: testapi, version: 1.0.0}
paths:
  /optional-number:
    post:
      operationId: optional_number
      parameters:
        - name: json_body
          in: query
          schema: {type: string}
      requestBody:
        content:
          application/json:
            schema: {type: number, nullable: true}
      responses:
        "204": {description: No content}
  /optional-integer:
    post:
      operationId: optional_integer
      requestBody:
        required: false
        content:
          application/json:
            schema: {type: integer, nullable: true}
      responses:
        "204": {description: No content}
  /optional-boolean:
    post:
      operationId: optional_boolean
      requestBody:
        content:
          application/json:
            schema: {type: boolean, nullable: true}
      responses:
        "204": {description: No content}
  /optional-string:
    post:
      operationId: optional_string
      requestBody:
        content:
          application/json:
            schema: {type: string, nullable: true}
      responses:
        "204": {description: No content}
"""


@with_generated_client_fixture(OPENAPI_30_SPEC)
class TestOpenAPI30NullableRequestBodies:
    def test_generated_package_type_checks_with_json_body_parameter(self, generated_client: Any) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "mypy", str(generated_client.output_path), "--strict"],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, result.stdout + result.stderr

    @pytest.mark.parametrize(
        ("operation", "ordinary", "ordinary_json", "falsy", "falsy_json"),
        [
            ("optional_number", 1.5, b"1.5", 0.0, b"0.0"),
            ("optional_integer", 7, b"7", 0, b"0"),
            ("optional_boolean", True, b"true", False, b"false"),
            ("optional_string", "present", b'"present"', "", b'""'),
        ],
    )
    def test_omitted_null_and_values_have_distinct_wire_representations(
        self,
        generated_client: Any,
        operation: str,
        ordinary: Any,
        ordinary_json: bytes,
        falsy: Any,
        falsy_json: bytes,
    ) -> None:
        endpoint = generated_client.import_module(f".api.default.{operation}")
        Client = generated_client.import_symbol(".client", "Client")
        UNSET = generated_client.import_symbol(".types", "UNSET")

        assert _sync_request(endpoint, Client).content == b""
        assert _sync_request(endpoint, Client, body=UNSET).content == b""
        assert _sync_request(endpoint, Client, body=None).content == b"null"
        assert _sync_request(endpoint, Client, body=ordinary).content == ordinary_json
        assert _sync_request(endpoint, Client, body=falsy).content == falsy_json


OPENAPI_31_SPEC = """
openapi: 3.1.0
info: {title: testapi, version: 1.0.0}
paths:
  /type-list:
    post:
      operationId: type_list
      requestBody:
        content:
          application/json:
            schema: {type: [number, "null"]}
      responses:
        "204": {description: No content}
  /any-of:
    post:
      operationId: any_of_nullable
      requestBody:
        content:
          application/json:
            schema:
              anyOf: [{type: integer}, {type: "null"}]
      responses:
        "204": {description: No content}
  /one-of:
    post:
      operationId: one_of_nullable
      requestBody:
        content:
          application/json:
            schema:
              oneOf: [{type: string}, {type: "null"}]
      responses:
        "204": {description: No content}
  /required-nullable:
    post:
      operationId: required_nullable
      requestBody:
        required: true
        content:
          application/problem+json:
            schema: {type: [boolean, "null"]}
      responses:
        "204": {description: No content}
  /optional-non-nullable:
    post:
      operationId: optional_non_nullable
      requestBody:
        required: false
        content:
          application/json:
            schema: {type: string}
      responses:
        "204": {description: No content}
  /required-non-nullable:
    post:
      operationId: required_non_nullable
      requestBody:
        required: true
        content:
          application/json:
            schema: {type: integer}
      responses:
        "204": {description: No content}
  /pass-through-union:
    post:
      operationId: pass_through_union
      requestBody:
        content:
          application/json:
            schema:
              anyOf: [{type: integer}, {type: string}]
      responses:
        "204": {description: No content}
  /date-time:
    post:
      operationId: nullable_date_time
      requestBody:
        content:
          application/json:
            schema:
              oneOf:
                - {type: string, format: date-time}
                - {type: "null"}
      responses:
        "204": {description: No content}
  /model:
    post:
      operationId: nullable_model
      requestBody:
        content:
          application/json:
            schema:
              oneOf:
                - {$ref: "#/components/schemas/Payload"}
                - {type: "null"}
      responses:
        "204": {description: No content}
  /array:
    post:
      operationId: nullable_array
      requestBody:
        content:
          application/json:
            schema:
              type: [array, "null"]
              items: {type: integer}
      responses:
        "204": {description: No content}
  /nested:
    post:
      operationId: nested_nullable_fields
      requestBody:
        required: true
        content:
          application/json:
            schema: {$ref: "#/components/schemas/NestedPayload"}
      responses:
        "204": {description: No content}
components:
  schemas:
    Payload:
      type: object
      properties:
        name: {type: string}
      required: [name]
    NestedPayload:
      type: object
      properties:
        optionalNullable: {type: [string, "null"]}
        optionalDateTime:
          type: [string, "null"]
          format: date-time
"""


@with_generated_client_fixture(OPENAPI_31_SPEC)
class TestOpenAPI31NullableRequestBodies:
    def _endpoint(self, generated_client: Any, operation: str) -> Any:
        return generated_client.import_module(f".api.default.{operation}")

    def test_type_list_and_composed_unions_preserve_presence(self, generated_client: Any) -> None:
        Client = generated_client.import_symbol(".client", "Client")
        UNSET = generated_client.import_symbol(".types", "UNSET")

        for operation, value, encoded in [
            ("type_list", 2.5, b"2.5"),
            ("any_of_nullable", 0, b"0"),
            ("one_of_nullable", "", b'""'),
        ]:
            endpoint = self._endpoint(generated_client, operation)
            assert _sync_request(endpoint, Client).content == b""
            assert _sync_request(endpoint, Client, body=UNSET).content == b""
            assert _sync_request(endpoint, Client, body=None).content == b"null"
            assert _sync_request(endpoint, Client, body=value).content == encoded

    def test_requiredness_and_nullability_are_independent_in_signatures(self, generated_client: Any) -> None:
        UNSET = generated_client.import_symbol(".types", "UNSET")

        def body_parameter(operation: str) -> inspect.Parameter:
            endpoint = self._endpoint(generated_client, operation)
            return inspect.signature(endpoint.sync_detailed).parameters["body"]

        required_nullable = body_parameter("required_nullable")
        optional_nullable = body_parameter("type_list")
        optional_non_nullable = body_parameter("optional_non_nullable")
        required_non_nullable = body_parameter("required_non_nullable")

        assert required_nullable.default is inspect.Parameter.empty
        assert type(None) in get_args(required_nullable.annotation)
        assert optional_nullable.default is UNSET
        assert type(None) in get_args(optional_nullable.annotation)
        assert optional_non_nullable.default is UNSET
        assert type(None) not in get_args(optional_non_nullable.annotation)
        assert required_non_nullable.default is inspect.Parameter.empty
        assert type(None) not in get_args(required_non_nullable.annotation)

    def test_non_nullable_requiredness_controls(self, generated_client: Any) -> None:
        Client = generated_client.import_symbol(".client", "Client")
        UNSET = generated_client.import_symbol(".types", "UNSET")

        optional = self._endpoint(generated_client, "optional_non_nullable")
        assert _sync_request(optional, Client).content == b""
        assert _sync_request(optional, Client, body=UNSET).content == b""
        assert _sync_request(optional, Client, body="").content == b'""'

        required = self._endpoint(generated_client, "required_non_nullable")
        assert _sync_request(required, Client, body=0).content == b"0"

    def test_required_nullable_uses_declared_json_media_type(self, generated_client: Any) -> None:
        Client = generated_client.import_symbol(".client", "Client")
        endpoint = self._endpoint(generated_client, "required_nullable")

        request = _sync_request(endpoint, Client, body=None)

        assert request.content == b"null"
        assert request.headers["Content-Type"] == "application/problem+json"
        assert _sync_request(endpoint, Client, body=False).content == b"false"

    def test_pass_through_and_transforming_union_members(self, generated_client: Any) -> None:
        Client = generated_client.import_symbol(".client", "Client")

        pass_through = self._endpoint(generated_client, "pass_through_union")
        assert _sync_request(pass_through, Client).content == b""
        assert _sync_request(pass_through, Client, body=0).content == b"0"
        assert _sync_request(pass_through, Client, body="value").content == b'"value"'

        date_time = self._endpoint(generated_client, "nullable_date_time")
        value = datetime.datetime(2026, 9, 15, 12, 30, tzinfo=datetime.UTC)
        assert _sync_request(date_time, Client).content == b""
        assert _sync_request(date_time, Client, body=None).content == b"null"
        assert _sync_request(date_time, Client, body=value).content == b'"2026-09-15T12:30:00+00:00"'

    def test_nullable_model_array_and_nested_fields(self, generated_client: Any) -> None:
        Client = generated_client.import_symbol(".client", "Client")
        Payload = generated_client.import_symbol(".models", "Payload")
        NestedPayload = generated_client.import_symbol(".models", "NestedPayload")

        model_endpoint = self._endpoint(generated_client, "nullable_model")
        assert _sync_request(model_endpoint, Client).content == b""
        assert _sync_request(model_endpoint, Client, body=None).content == b"null"
        assert json.loads(_sync_request(model_endpoint, Client, body=Payload(name="Ada")).content) == {"name": "Ada"}

        array_endpoint = self._endpoint(generated_client, "nullable_array")
        assert _sync_request(array_endpoint, Client).content == b""
        assert _sync_request(array_endpoint, Client, body=None).content == b"null"
        assert json.loads(_sync_request(array_endpoint, Client, body=[]).content) == []
        assert json.loads(_sync_request(array_endpoint, Client, body=[0, 2]).content) == [0, 2]

        nested_endpoint = self._endpoint(generated_client, "nested_nullable_fields")
        assert json.loads(_sync_request(nested_endpoint, Client, body=NestedPayload()).content) == {}
        assert json.loads(
            _sync_request(nested_endpoint, Client, body=NestedPayload(optional_nullable=None)).content
        ) == {"optionalNullable": None}
        date_time = datetime.datetime(2026, 9, 15, 12, 30, tzinfo=datetime.UTC)
        assert json.loads(
            _sync_request(nested_endpoint, Client, body=NestedPayload(optional_date_time=date_time)).content
        ) == {"optionalDateTime": "2026-09-15T12:30:00+00:00"}

    def test_async_transport_preserves_presence(self, generated_client: Any) -> None:
        Client = generated_client.import_symbol(".client", "Client")
        UNSET = generated_client.import_symbol(".types", "UNSET")
        endpoint = self._endpoint(generated_client, "any_of_nullable")

        assert _async_request(endpoint, Client).content == b""
        assert _async_request(endpoint, Client, body=UNSET).content == b""
        assert _async_request(endpoint, Client, body=None).content == b"null"
        assert _async_request(endpoint, Client, body=0).content == b"0"
