import json
from unittest.mock import MagicMock

import httpx
import pytest

from end_to_end_tests.functional_tests.helpers import (
    assert_model_decode_encode,
    assert_model_property_type_hint,
    with_generated_client_fixture,
    with_generated_code_import,
    with_generated_code_imports,
)


@with_generated_client_fixture(
    """
components:
  schemas:
    StringOrInt:
      type: ["string", "integer"]
    MyModel:
      type: object
      properties:
        stringOrIntProp:
          type: ["string", "integer"]
"""
)
@with_generated_code_imports(
    ".models.MyModel",
)
class TestSimpleTypeList:
    def test_decode_encode(self, MyModel):
        assert_model_decode_encode(MyModel, {"stringOrIntProp": "a"}, MyModel(string_or_int_prop="a"))
        assert_model_decode_encode(MyModel, {"stringOrIntProp": 1}, MyModel(string_or_int_prop=1))

    def test_type_hints(self, MyModel):
        assert_model_property_type_hint(MyModel, "string_or_int_prop", "int | str | Unset")


@with_generated_client_fixture(
    """
components:
  schemas:
    ThingA:
      type: object
      properties:
        propA: { type: "string" }
      required: ["propA"]
    ThingB:
      type: object
      properties:
        propB: { type: "string" }
      required: ["propB"]
    ThingAOrB:
      oneOf:
        - $ref: "#/components/schemas/ThingA"
        - $ref: "#/components/schemas/ThingB"
    ModelWithUnion:
      type: object
      properties:
        thing: {"$ref": "#/components/schemas/ThingAOrB"}
        thingOrString:
          oneOf:
            - $ref: "#/components/schemas/ThingA"
            - type: string
    ModelWithRequiredUnion:
      type: object
      properties:
        thing: {"$ref": "#/components/schemas/ThingAOrB"}
      required: ["thing"]
    ModelWithNestedUnion:
      type: object
      properties:
        thingOrValue:
          oneOf:
            - "$ref": "#/components/schemas/ThingAOrB"
            - oneOf:
              - type: string
              - type: number
    ModelWithUnionOfOne:
      type: object
      properties:
        thing:
          oneOf:
            - $ref: "#/components/schemas/ThingA"
        requiredThing:
          oneOf:
            - $ref: "#/components/schemas/ThingA"
      required: ["requiredThing"]
"""
)
@with_generated_code_imports(
    ".models.ThingA",
    ".models.ThingB",
    ".models.ModelWithUnion",
    ".models.ModelWithRequiredUnion",
    ".models.ModelWithNestedUnion",
    ".models.ModelWithUnionOfOne",
)
class TestOneOf:
    def test_disambiguate_objects_via_required_properties(self, ThingA, ThingB, ModelWithUnion):
        assert_model_decode_encode(
            ModelWithUnion,
            {"thing": {"propA": "x"}},
            ModelWithUnion(thing=ThingA(prop_a="x")),
        )
        assert_model_decode_encode(
            ModelWithUnion,
            {"thing": {"propB": "x"}},
            ModelWithUnion(thing=ThingB(prop_b="x")),
        )

    def test_disambiguate_object_and_non_object(self, ThingA, ModelWithUnion):
        assert_model_decode_encode(
            ModelWithUnion,
            {"thingOrString": {"propA": "x"}},
            ModelWithUnion(thing_or_string=ThingA(prop_a="x")),
        )
        assert_model_decode_encode(
            ModelWithUnion,
            {"thingOrString": "x"},
            ModelWithUnion(thing_or_string="x"),
        )

    def test_disambiguate_nested_union(self, ThingA, ThingB, ModelWithNestedUnion):
        assert_model_decode_encode(
            ModelWithNestedUnion,
            {"thingOrValue": {"propA": "x"}},
            ModelWithNestedUnion(thing_or_value=ThingA(prop_a="x")),
        )
        assert_model_decode_encode(
            ModelWithNestedUnion,
            {"thingOrValue": 3},
            ModelWithNestedUnion(thing_or_value=3),
        )

    def test_type_hints(self, ModelWithUnion, ModelWithRequiredUnion, ModelWithUnionOfOne, ThingA):
        assert_model_property_type_hint(
            ModelWithUnion,
            "thing",
            "ThingA | ThingB | Unset",
        )
        assert_model_property_type_hint(
            ModelWithRequiredUnion,
            "thing",
            "ThingA | ThingB",
        )
        assert_model_property_type_hint(ModelWithUnionOfOne, "thing", "ThingA | Unset")
        assert_model_property_type_hint(ModelWithUnionOfOne, "required_thing", "ThingA")


@with_generated_client_fixture(
    """
components:
  schemas:
    ThingA:
      type: object
      properties:
        propA: { type: "string" }
      required: ["propA"]
    ModelWithConstUnions:
      type: object
      properties:
        sizeOrAuto:
          anyOf:
            - const: "auto"
            - type: integer
        thingOrNone:
          oneOf:
            - const: "none"
            - $ref: "#/components/schemas/ThingA"
        mixedConsts:
          anyOf:
            - const: 1
            - const: "one"
            - type: boolean
"""
)
@with_generated_code_imports(
    ".models.ModelWithConstUnions",
    ".models.ThingA",
)
class TestUnionsWithConst:
    """Regression tests for https://github.com/openapi-generators/openapi-python-client/issues/1263"""

    def test_const_variant_matches(self, ModelWithConstUnions):
        assert_model_decode_encode(
            ModelWithConstUnions,
            {"sizeOrAuto": "auto", "thingOrNone": "none", "mixedConsts": "one"},
            ModelWithConstUnions(size_or_auto="auto", thing_or_none="none", mixed_consts="one"),
        )
        assert_model_decode_encode(
            ModelWithConstUnions,
            {"mixedConsts": 1},
            ModelWithConstUnions(mixed_consts=1),
        )

    def test_falls_through_const_to_later_variants(self, ModelWithConstUnions, ThingA):
        assert_model_decode_encode(
            ModelWithConstUnions,
            {"sizeOrAuto": 5, "thingOrNone": {"propA": "x"}, "mixedConsts": True},
            ModelWithConstUnions(size_or_auto=5, thing_or_none=ThingA(prop_a="x"), mixed_consts=True),
        )

    def test_wrong_value_of_right_type_is_not_accepted_as_const(self, ModelWithConstUnions):
        with pytest.raises(TypeError):
            ModelWithConstUnions.from_dict({"thingOrNone": "something else"})

    def test_type_hints(self, ModelWithConstUnions):
        assert_model_property_type_hint(ModelWithConstUnions, "size_or_auto", "int | Literal['auto'] | Unset")


@with_generated_client_fixture(
    """
paths:
  "/thing":
    get:
      operationId: getThing
      responses:
        "200":
          description: Success
          content:
            application/json:
              schema:
                anyOf:
                  - const: "Why have a fixed response? I dunno"
                  - $ref: "#/components/schemas/Thing"
components:
  schemas:
    Thing:
      type: object
      properties:
        value: { type: "string" }
      required: ["value"]
"""
)
@with_generated_code_imports(
    ".api.default.get_thing.sync",
    ".client.Client",
    ".models.Thing",
)
class TestResponseUnionWithConst:
    """Regression tests for https://github.com/openapi-generators/openapi-python-client/issues/1263"""

    @staticmethod
    def _client_returning(Client, body):
        mock_httpx_client = MagicMock(spec=httpx.Client)
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = body
        mock_response.content = json.dumps(body).encode()
        mock_response.headers = {}
        mock_httpx_client.request.return_value = mock_response
        client = Client(base_url="https://api.example.com")
        client.set_httpx_client(mock_httpx_client)
        return client

    def test_parses_const_variant(self, sync, Client):
        client = self._client_returning(Client, "Why have a fixed response? I dunno")
        assert sync(client=client) == "Why have a fixed response? I dunno"

    def test_parses_model_variant(self, sync, Client, Thing):
        client = self._client_returning(Client, {"value": "x"})
        assert sync(client=client) == Thing(value="x")


@with_generated_client_fixture(
    """
paths:
  "/upload":
    post:
      operationId: upload
      requestBody:
        content:
          multipart/form-data:
            schema:
              $ref: "#/components/schemas/Form"
      responses:
        "200":
          description: Success
components:
  schemas:
    Form:
      type: object
      properties:
        sizeOrAuto:
          anyOf:
            - const: "auto"
            - type: integer
"""
)
@with_generated_code_import(".models.Form")
class TestMultipartUnionWithConst:
    def test_to_multipart(self, Form):
        assert Form(size_or_auto="auto").to_multipart() == [("sizeOrAuto", (None, "auto", "text/plain"))]
        assert Form(size_or_auto=3).to_multipart() == [("sizeOrAuto", (None, b"3", "text/plain"))]
