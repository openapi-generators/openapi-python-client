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
# Various use cases for oneOf

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
# Various use cases for a oneOf where one of the variants is null, since these are handled
# a bit differently in the generator

components:
  schemas:
    MyEnum:
      type: string
      enum: ["a", "b"]
    MyObject:
      type: object
      properties:
        name:
          type: string
    MyModel:
      properties:
        nullableEnumProp:
          oneOf:
            - {"$ref": "#/components/schemas/MyEnum"}
            - type: "null"
        nullableObjectProp:
          oneOf:
            - {"$ref": "#/components/schemas/MyObject"}
            - type: "null"
        inlineNullableObject:
          # Note, the generated class for this should be called "MyModelInlineNullableObject",
          # since the generator's rule for inline schemas that require their own class is to
          # concatenate the property name to the parent schema name.
          oneOf:
            - type: object
              properties:
                name:
                  type: string
            - type: "null"
""")
@with_generated_code_imports(
    ".models.MyEnum",
    ".models.MyObject",
    ".models.MyModel",
    ".models.MyModelInlineNullableObject",
    ".types.Unset",
)
class TestUnionsWithNull:
    def test_nullable_enum_prop(self, MyModel, MyEnum):
        assert_model_decode_encode(MyModel, {"nullableEnumProp": "b"}, MyModel(nullable_enum_prop=MyEnum.B))
        assert_model_decode_encode(MyModel, {"nullableEnumProp": None}, MyModel(nullable_enum_prop=None))

    def test_nullable_object_prop(self, MyModel, MyObject):
        assert_model_decode_encode( MyModel, {"nullableObjectProp": None}, MyModel(nullable_object_prop=None))
        assert_model_decode_encode( MyModel, {"nullableObjectProp": None}, MyModel(nullable_object_prop=None))

    def test_nullable_object_prop_with_inline_schema(self, MyModel, MyModelInlineNullableObject):
        assert_model_decode_encode(
            MyModel,
            {"inlineNullableObject": {"name": "a"}},
            MyModel(inline_nullable_object=MyModelInlineNullableObject(name="a")),
        )
        assert_model_decode_encode( MyModel, {"inlineNullableObject": None}, MyModel(inline_nullable_object=None))
    
    def test_type_hints(self, MyModel, MyEnum, Unset):
        assert_model_property_type_hint(MyModel, "nullable_enum_prop", Union[MyEnum, None, Unset])
        assert_model_property_type_hint(MyModel, "nullable_object_prop", Union[ForwardRef("MyObject"), None, Unset])
        assert_model_property_type_hint(
            MyModel,
            "inline_nullable_object",
            Union[ForwardRef("MyModelInlineNullableObject"), None, Unset],
        )


@with_generated_client_fixture(
"""
# Tests for combining the OpenAPI 3.0 "nullable" attribute with an enum

openapi: 3.0.0

components:
  schemas:
    MyEnum:
      type: string
      enum: ["a", "b"]
    MyEnumIncludingNull:
      type: string
      nullable: true
      enum: ["a", "b", null]
    MyModel:
      properties:
        nullableEnumProp:
          allOf:
            - {"$ref": "#/components/schemas/MyEnum"}
          nullable: true
        enumIncludingNullProp: {"$ref": "#/components/schemas/MyEnumIncludingNull"}
""")
@with_generated_code_imports(
    ".models.MyEnum",
    ".models.MyEnumIncludingNull",
    ".models.MyModel",
    ".types.Unset",
)
class TestNullableEnumsInOpenAPI30:
    def test_nullable_enum_prop(self, MyModel, MyEnum, MyEnumIncludingNull):
        assert_model_decode_encode(MyModel, {"nullableEnumProp": "b"}, MyModel(nullable_enum_prop=MyEnum.B))
        assert_model_decode_encode(MyModel, {"nullableEnumProp": None}, MyModel(nullable_enum_prop=None))
        assert_model_decode_encode(
            MyModel,
            {"enumIncludingNullProp": "a"},
            MyModel(enum_including_null_prop=MyEnumIncludingNull.A),
        )
        assert_model_decode_encode( MyModel, {"enumIncludingNullProp": None}, MyModel(enum_including_null_prop=None))
    
    def test_type_hints(self, MyModel, MyEnum, MyEnumIncludingNull, Unset):
        assert_model_property_type_hint(MyModel, "nullable_enum_prop", Union[MyEnum, None, Unset])
        assert_model_property_type_hint(MyModel, "enum_including_null_prop", Union[MyEnumIncludingNull, None, Unset])


@with_generated_client_fixture(
"""
# Tests for using a discriminator property

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


@with_generated_client_fixture(
"""
# Tests for using multiple values of "type:" in one schema (OpenAPI 3.1)

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
class TestListOfSimpleTypes:
    def test_decode_encode(self, MyModel):
        assert_model_decode_encode(MyModel, {"stringOrIntProp": "a"}, MyModel(string_or_int_prop="a"))
        assert_model_decode_encode(MyModel, {"stringOrIntProp": 1}, MyModel(string_or_int_prop=1))

    def test_type_hints(self, MyModel, Unset):
        assert_model_property_type_hint(MyModel, "string_or_int_prop", Union[str, int, Unset])


@with_generated_client_fixture(
"""
# Test cases where there's a union of types *and* an explicit list of multiple "type:"s -
# there was a bug where this could cause enum/model classes to be generated incorrectly

components:
  schemas:
    MyStringEnum:
      type: string
      enum: ["a", "b"]
    MyIntEnum:
      type: integer
      enum: [1, 2]
    MyEnumIncludingNull:
      type: ["string", "null"]
      enum: ["a", "b", null]
    MyObject:
      type: object
      properties:
        name:
          type: string
    MyModel:
      properties:
        enumsWithListOfTypesProp:
          type: ["string", "integer"]
          oneOf:
            - {"$ref": "#/components/schemas/MyStringEnum"}
            - {"$ref": "#/components/schemas/MyIntEnum"}
        enumIncludingNullProp: {"$ref": "#/components/schemas/MyEnumIncludingNull"}
        nullableObjectWithListOfTypesProp:
          type: ["string", "object"]
          oneOf:
            - {"$ref": "#/components/schemas/MyObject"}
            - type: "null"
""")
@with_generated_code_imports(
    ".models.MyStringEnum",
    ".models.MyIntEnum",
    ".models.MyEnumIncludingNull",
    ".models.MyObject",
    ".models.MyModel",
    ".types.Unset",
)
class TestUnionsWithListOfSimpleTypes:
    def test_union_of_enums(self, MyModel, MyStringEnum, MyIntEnum):
        assert_model_decode_encode(
            MyModel,
            {"enumsWithListOfTypesProp": "b"},
            MyModel(enums_with_list_of_types_prop=MyStringEnum.B),
        )
        assert_model_decode_encode(
            MyModel,
            {"enumsWithListOfTypesProp": 2},
            MyModel(enums_with_list_of_types_prop=MyIntEnum.VALUE_2),
        )

    def test_union_of_enum_with_null(self, MyModel, MyEnumIncludingNull):
        assert_model_decode_encode(
            MyModel,
            {"enumIncludingNullProp": "b"},
            MyModel(enum_including_null_prop=MyEnumIncludingNull.B),
        )
        assert_model_decode_encode(
            MyModel,
            {"enumIncludingNullProp": None},
            MyModel(enum_including_null_prop=None),
        )

    def test_nullable_object_with_list_of_types(self, MyModel, MyObject):
        assert_model_decode_encode(
            MyModel,
            {"nullableObjectWithListOfTypesProp": {"name": "a"}},
            MyModel(nullable_object_with_list_of_types_prop=MyObject(name="a")),
        )
        assert_model_decode_encode(
            MyModel,
            {"nullableObjectWithListOfTypesProp": None},
            MyModel(nullable_object_with_list_of_types_prop=None),
        )
