
import pytest
from end_to_end_tests.end_to_end_test_helpers import (
    assert_bad_schema_warning,
    assert_model_decode_encode,
    inline_spec_should_cause_warnings,
    with_generated_client_fixture,
    with_generated_code_imports,
)


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
    ModelWithUnion:
      type: object
      properties:
        thing:
          oneOf:
            - $ref: "#/components/schemas/ThingA"
            - $ref: "#/components/schemas/ThingB"
        thingOrString:
          oneOf:
            - $ref: "#/components/schemas/ThingA"
            - type: string
    ModelWithNestedUnion:
      type: object
      properties:
        thingOrValue:
          oneOf:
            - oneOf:
              - $ref: "#/components/schemas/ThingA"
              - $ref: "#/components/schemas/ThingB"
            - oneOf:
              - type: string
              - type: number
""")
@with_generated_code_imports(
    ".models.ThingA",
    ".models.ThingB",
    ".models.ModelWithUnion",
    ".models.ModelWithNestedUnion",
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


class TestUnionInvalidSchemas:
    @pytest.fixture(scope="class")
    def warnings(self):
        return inline_spec_should_cause_warnings(
"""
components:
  schemas:
    UnionWithInvalidReference:
      anyOf:
        - $ref: "#/components/schemas/DoesntExist"
    UnionWithInvalidDefault:
      type: ["number", "integer"]
      default: aaa
"""
        )

    def test_invalid_reference(self, warnings):
        assert_bad_schema_warning(warnings, "UnionWithInvalidReference", "Could not find reference")

    def test_invalid_default(self, warnings):
        assert_bad_schema_warning(warnings, "UnionWithInvalidDefault", "Invalid int value: aaa")
