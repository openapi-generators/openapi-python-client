from typing import Any

import pytest

from end_to_end_tests.functional_tests.helpers import (
    with_generated_client_fixture,
    with_generated_code_import,
)


class DocstringParser:
    lines: list[str]

    def __init__(self, item: Any):
        self.lines = [line.lstrip() for line in item.__doc__.split("\n")]

    def get_section(self, header_line: str) -> list[str]:
        lines = self.lines[self.lines.index(header_line) + 1 :]
        return lines[0 : lines.index("")]


@with_generated_client_fixture(
    """
components:
  schemas:
    MyModel:
      description: I like this type.
      type: object
      properties:
        reqStr:
          type: string
          description: This is necessary.
        optStr:
          type: string
          description: This isn't necessary.
        undescribedProp:
          type: string
      required: ["reqStr", "undescribedProp"]
"""
)
@with_generated_code_import(".models.MyModel")
class TestSchemaDocstrings:
    def test_model_description(self, MyModel):
        assert DocstringParser(MyModel).lines[0] == "I like this type."

    def test_model_properties(self, MyModel):
        assert set(DocstringParser(MyModel).get_section("Attributes:")) == {
            "req_str (str): This is necessary.",
            "opt_str (str | Unset): This isn't necessary.",
            "undescribed_prop (str):",
        }


@with_generated_client_fixture(
    """
tags:
    - name: service1
paths:
  "/simple":
    get:
      operationId: getSimpleThing
      description: Get a simple thing.
      responses:
        "200":
          description: Success!
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/GoodResponse"
      tags:
        - service1
    post:
      operationId: postSimpleThing
      description: Post a simple thing.
      requestBody:
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/Thing"
      responses:
        "200":
          description: Success!
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/GoodResponse"
        "400":
          description: Failure!!
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
      tags:
        - service1
  "/simple/{id}/{index}":
    get:
      operationId: getAttributeByIndex
      description: Get a simple thing's attribute.
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            description: Which one.
        - name: index
          in: path
          required: true
          schema:
            type: integer
        - name: fries
          in: query
          required: false
          schema:
            type: boolean
            description: Do you want fries with that?
      responses:
        "200":
          description: Success!
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/GoodResponse"
      tags:
        - service1

components:
  schemas:
    GoodResponse:
      type: object
    ErrorResponse:
      type: object
    Thing:
      type: object
      description: The thing.
"""
)
@with_generated_code_import(".api.service1.get_simple_thing.sync", alias="get_simple_thing_sync")
@with_generated_code_import(".api.service1.post_simple_thing.sync", alias="post_simple_thing_sync")
@with_generated_code_import(".api.service1.get_attribute_by_index.sync", alias="get_attribute_by_index_sync")
class TestEndpointDocstrings:
    def test_description(self, get_simple_thing_sync):
        assert DocstringParser(get_simple_thing_sync).lines[0] == "Get a simple thing."

    def test_response_single_type(self, get_simple_thing_sync):
        assert DocstringParser(get_simple_thing_sync).get_section("Returns:") == [
            "GoodResponse",
        ]

    def test_response_union_type(self, post_simple_thing_sync):
        returns_line = DocstringParser(post_simple_thing_sync).get_section("Returns:")[0]
        assert returns_line in (
            "GoodResponse | ErrorResponse",
            "ErrorResponse | GoodResponse",
        )

    def test_request_body(self, post_simple_thing_sync):
        assert DocstringParser(post_simple_thing_sync).get_section("Args:") == ["body (Thing | Unset): The thing."]

    def test_params(self, get_attribute_by_index_sync):
        assert DocstringParser(get_attribute_by_index_sync).get_section("Args:") == [
            "id (str): Which one.",
            "index (int):",
            "fries (bool | Unset): Do you want fries with that?",
        ]


@with_generated_client_fixture(
    """
paths:
  /tasks/{id}:
    parameters:
      - name: id
        in: path
        required: true
        description: Task to export.
        schema:
          type: string
          description: A task identifier.
    get:
      operationId: exportTasks
      parameters:
        - name: since
          in: query
          description: Only include tasks changed after this timestamp.
          schema:
            type: integer
            description: Unix timestamp in milliseconds.
        - name: empty
          in: query
          description: ""
          schema:
            type: string
            description: Schema fallback.
        - name: undescribed
          in: query
          schema:
            type: string
        - name: trace
          in: header
          description: Trace this export.
          schema:
            type: string
        - name: session
          in: cookie
          description: Session for this export.
          schema:
            type: string
        - $ref: "#/components/parameters/State"
        - name: filters
          in: query
          description: Filter the exported tasks.
          schema:
            $ref: "#/components/schemas/Filters"
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Filters"
  /other:
    get:
      operationId: getOther
      parameters:
        - name: filters
          in: query
          schema:
            $ref: "#/components/schemas/Filters"
      responses:
        "200":
          description: OK
components:
  parameters:
    State:
      name: state
      in: query
      description: Select tasks in this state.
      schema:
        $ref: "#/components/schemas/State"
  schemas:
    State:
      type: string
      enum: [open, closed]
      description: A task state.
    Filters:
      type: object
      description: Reusable task filters.
      properties:
        label:
          type: string
          description: A task label.
"""
)
class TestParameterDocstrings:
    @pytest.mark.parametrize("function_name", ["sync", "sync_detailed", "asyncio", "asyncio_detailed"])
    def test_parameter_descriptions(self, generated_client, function_name):
        function = generated_client.import_symbol(".api.default.export_tasks", function_name)
        assert set(DocstringParser(function).get_section("Args:")) == {
            "id (str): Task to export.",
            "since (int | Unset): Only include tasks changed after this timestamp.",
            "empty (str | Unset): Schema fallback.",
            "undescribed (str | Unset):",
            "trace (str | Unset): Trace this export.",
            "session (str | Unset): Session for this export.",
            "state (State | Unset): Select tasks in this state.",
            "filters (Filters | Unset): Filter the exported tasks.",
        }

    def test_shared_schema_descriptions(self, generated_client):
        filters = generated_client.import_symbol(".models.filters", "Filters")
        assert DocstringParser(filters).lines[0] == "Reusable task filters."
        assert DocstringParser(filters).get_section("Attributes:") == ["label (str | Unset): A task label."]

        function = generated_client.import_symbol(".api.default.get_other", "sync_detailed")
        assert DocstringParser(function).get_section("Args:") == ["filters (Filters | Unset): Reusable task filters."]
