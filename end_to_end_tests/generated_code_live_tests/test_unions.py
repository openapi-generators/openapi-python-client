
from end_to_end_tests.end_to_end_test_helpers import (
    assert_model_decode_encode,
    with_generated_code_import,
    with_generated_client_fixture,
)


@with_generated_client_fixture(
"""
paths: {}
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
""")
@with_generated_code_import(".models.ThingA")
@with_generated_code_import(".models.ThingB")
@with_generated_code_import(".models.ModelWithUnion")
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
