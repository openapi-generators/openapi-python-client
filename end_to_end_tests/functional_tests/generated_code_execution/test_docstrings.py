import re
from typing import Any, List

from end_to_end_tests.functional_tests.helpers import (
    with_generated_code_import,
    with_generated_client_fixture,
)
from end_to_end_tests.generated_client import GeneratedClientContext


class DocstringParser:
    lines: List[str]

    def __init__(self, item: Any):
        self.lines = [line.lstrip() for line in item.__doc__.split("\n")]

    def get_section(self, header_line: str) -> List[str]:
        lines = self.lines[self.lines.index(header_line)+1:]
        return lines[0:lines.index("")]


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
""")
@with_generated_code_import(".models.MyModel")
class TestSchemaDocstringsDefaultBehavior:
    def test_model_description(self, MyModel):
        assert DocstringParser(MyModel).lines[0] == "I like this type."

    def test_model_properties_in_model_description(self, MyModel):
        assert set(DocstringParser(MyModel).get_section("Attributes:")) == {
            "req_str (str): This is necessary.",
            "opt_str (Union[Unset, str]): This isn't necessary.",
            "undescribed_prop (str):",
        }


@with_generated_client_fixture(
"""
components:
  schemas:
    MyModel:
      description: I like this type.
      type: object
      properties:
        prop1:
          type: string
          description: This attribute has a description
        prop2:
          type: string  # no description for this one
      required: ["prop1", "prop2"]
""",
config="docstrings_on_attributes: true",
)
@with_generated_code_import(".models.MyModel")
class TestSchemaWithDocstringsOnAttributesOption:
    def test_model_description_is_entire_docstring(self, MyModel):
        assert MyModel.__doc__.strip() == "I like this type."

    def test_attrs_have_docstrings(self, generated_client: GeneratedClientContext):
        # A docstring that appears after an attribute is *not* stored in __doc__ anywhere
        # by the interpreter, so we can't inspect it that way-- but it's still valid for it
        # to appear there, and it will be recognized by documentation tools. So we'll assert
        # that these strings appear in the source code. The code should look like this:
        #     class MyModel:
        #         """I like this type."""
        #         prop1: str
        #         """This attribute has a description"""
        #         prop2: str
        # 
        source_file_path = generated_client.output_path / generated_client.base_module / "models" / "my_model.py"
        content = source_file_path.read_text()
        assert re.search('\n *prop1: *str\n *""" *This attribute has a description *"""\n', content)
        assert re.search('\n *prop2: *str\n *[^"]', content)


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
""")
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
            "Union[GoodResponse, ErrorResponse]",
            "Union[ErrorResponse, GoodResponse]",
        )

    def test_request_body(self, post_simple_thing_sync):
        assert DocstringParser(post_simple_thing_sync).get_section("Args:") == [
            "body (Thing): The thing."
        ]

    def test_params(self, get_attribute_by_index_sync):
        assert DocstringParser(get_attribute_by_index_sync).get_section("Args:") == [
            "id (str): Which one.",
            "index (int):",
            "fries (Union[Unset, bool]): Do you want fries with that?",
        ]
