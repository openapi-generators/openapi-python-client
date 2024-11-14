from typing import ForwardRef, Union

import pytest

from end_to_end_tests.functional_tests.helpers import (
    assert_model_decode_encode,
    assert_model_property_type_hint,
    with_generated_client_fixture,
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
    ".types.Unset"
)
class TestSimpleTypeList:
    def test_decode_encode(self, MyModel):
        assert_model_decode_encode(MyModel, {"stringOrIntProp": "a"}, MyModel(string_or_int_prop="a"))
        assert_model_decode_encode(MyModel, {"stringOrIntProp": 1}, MyModel(string_or_int_prop=1))

    def test_type_hints(self, MyModel, Unset):
        assert_model_property_type_hint(MyModel, "string_or_int_prop", Union[str, int, Unset])


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
""")
@with_generated_code_imports(
    ".models.ThingA",
    ".models.ThingB",
    ".models.ModelWithUnion",
    ".models.ModelWithRequiredUnion",
    ".models.ModelWithNestedUnion",
    ".models.ModelWithUnionOfOne",
    ".types.Unset"
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

    def test_type_hints(self, ModelWithUnion, ModelWithRequiredUnion, ModelWithUnionOfOne, ThingA, Unset):
        assert_model_property_type_hint(
            ModelWithUnion,
            "thing",
            Union[ForwardRef("ThingA"), ForwardRef("ThingB"), Unset],
        )
        assert_model_property_type_hint(
            ModelWithRequiredUnion,
            "thing",
            Union[ForwardRef("ThingA"), ForwardRef("ThingB")],
        )
        assert_model_property_type_hint(
            ModelWithUnionOfOne, "thing", Union[ForwardRef("ThingA"), Unset]
        )
        assert_model_property_type_hint(
            ModelWithUnionOfOne, "required_thing", "ThingA"
        )


@with_generated_client_fixture(
"""
components:
  schemas:
    ModelType1:
      type: object
      properties:
        modelType: {"type": "string"}
        name: {"type": "string"}
      required: ["modelType"]
    ModelType2:
      type: object
      properties:
        modelType: {"type": "string"}
        name: {"type": "string"}
      required: ["modelType"]
    Corgi:
      type: object
      properties:
        modelType: {"type": "string"}
        dogType: {"type": "string"}
        name: {"type": "string"}
      required: ["modelType"]
    Schnauzer:
      type: object
      properties:
        modelType: {"type": "string"}
        dogType: {"type": "string"}
        name: {"type": "string"}
      required: ["modelType"]
    WithDiscriminatedUnion:
      type: object
      properties:
        unionProp:
          oneOf:
            - $ref: "#/components/schemas/ModelType1"
            - $ref: "#/components/schemas/ModelType2"
          discriminator:
            propertyName: modelType
            mapping:
              "type1": "#/components/schemas/ModelType1"
              "type2": "ModelType2"  # exactly equivalent to "#/components/schemas/ModelType2"
              "another-value": "#/components/schemas/ModelType2"  # deliberately mapped to same type as previous line
    WithDiscriminatedUnionImplicitMapping:
      type: object
      properties:
        unionProp:
          oneOf:
            - $ref: "#/components/schemas/ModelType1"
            - $ref: "#/components/schemas/ModelType2"
          discriminator:
            propertyName: modelType
    WithNestedDiscriminatorsSameProperty:
      type: object
      properties:
        unionProp:
          oneOf:
            - oneOf:
              - $ref: "#/components/schemas/ModelType1"
              - $ref: "#/components/schemas/ModelType2"
              discriminator:
                propertyName: modelType
            - oneOf:
              - $ref: "#/components/schemas/Corgi"
              - $ref: "#/components/schemas/Schnauzer"
              discriminator:
                propertyName: modelType
    WithNestedDiscriminatorsDifferentProperty:
      type: object
      properties:
        unionProp:
          oneOf:
            - oneOf:
              - $ref: "#/components/schemas/ModelType1"
              - $ref: "#/components/schemas/ModelType2"
              discriminator:
                propertyName: modelType
            - oneOf:
              - $ref: "#/components/schemas/Corgi"
              - $ref: "#/components/schemas/Schnauzer"
              discriminator:
                propertyName: dogType
""")
@with_generated_code_imports(
    ".models.ModelType1",
    ".models.ModelType2",
    ".models.Corgi",
    ".models.Schnauzer",
    ".models.WithDiscriminatedUnion",
    ".models.WithDiscriminatedUnionImplicitMapping",
    ".models.WithNestedDiscriminatorsSameProperty",
    ".models.WithNestedDiscriminatorsDifferentProperty",
)
class TestDiscriminators:
    def test_with_explicit_mapping(self, ModelType1, ModelType2, WithDiscriminatedUnion):
        assert_model_decode_encode(
            WithDiscriminatedUnion,
            {"unionProp": {"modelType": "type1", "name": "a"}},
            WithDiscriminatedUnion(union_prop=ModelType1(model_type="type1", name="a")),
        )
        assert_model_decode_encode(
            WithDiscriminatedUnion,
            {"unionProp": {"modelType": "type2", "name": "a"}},
            WithDiscriminatedUnion(union_prop=ModelType2(model_type="type2", name="a")),
        )
        assert_model_decode_encode(
            WithDiscriminatedUnion,
            {"unionProp": {"modelType": "another-value", "name": "a"}},
            WithDiscriminatedUnion(union_prop=ModelType2(model_type="another-value", name="a")),
        )
        with pytest.raises(TypeError):
            WithDiscriminatedUnion.from_dict({"unionProp": {"modelType": "ModelType1"}})
        with pytest.raises(TypeError):
            WithDiscriminatedUnion.from_dict({"unionProp": {"modelType": "unknown-value"}})

    def test_with_implicit_mapping(self, ModelType1, ModelType2, WithDiscriminatedUnionImplicitMapping):
        assert_model_decode_encode(
            WithDiscriminatedUnionImplicitMapping,
            {"unionProp": {"modelType": "ModelType1", "name": "a"}},
            WithDiscriminatedUnionImplicitMapping(union_prop=ModelType1(model_type="ModelType1", name="a")),
        )
        assert_model_decode_encode(
            WithDiscriminatedUnionImplicitMapping,
            {"unionProp": {"modelType": "ModelType2", "name": "a"}},
            WithDiscriminatedUnionImplicitMapping(union_prop=ModelType2(model_type="ModelType2", name="a")),
        )
        with pytest.raises(TypeError):
            WithDiscriminatedUnionImplicitMapping.from_dict({"unionProp": {"modelType": "unknown-value"}})

    def test_nested_with_same_property(self, ModelType1, Schnauzer, WithNestedDiscriminatorsSameProperty):
        assert_model_decode_encode(
            WithNestedDiscriminatorsSameProperty,
            {"unionProp": {"modelType": "ModelType1", "name": "a"}},
            WithNestedDiscriminatorsSameProperty(union_prop=ModelType1(model_type="ModelType1", name="a")),
        )
        assert_model_decode_encode(
            WithNestedDiscriminatorsSameProperty,
            {"unionProp": {"modelType": "Schnauzer", "name": "a"}},
            WithNestedDiscriminatorsSameProperty(union_prop=Schnauzer(model_type="Schnauzer", name="a")),
        )

    def test_nested_with_different_property(self, ModelType1, Schnauzer, WithNestedDiscriminatorsDifferentProperty):
        assert_model_decode_encode(
            WithNestedDiscriminatorsDifferentProperty,
            {"unionProp": {"modelType": "ModelType1", "name": "a"}},
            WithNestedDiscriminatorsDifferentProperty(union_prop=ModelType1(model_type="ModelType1", name="a")),
        )
        assert_model_decode_encode(
            WithNestedDiscriminatorsDifferentProperty,
            {"unionProp": {"modelType": "irrelevant", "dogType": "Schnauzer", "name": "a"}},
            WithNestedDiscriminatorsDifferentProperty(union_prop=Schnauzer(model_type="irrelevant", dog_type="Schnauzer", name="a")),
        )
