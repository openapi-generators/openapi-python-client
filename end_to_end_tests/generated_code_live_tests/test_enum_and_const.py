
from typing import Any
import pytest
from end_to_end_tests.end_to_end_test_helpers import (
    assert_bad_schema_warning,
    assert_model_decode_encode,
    inline_spec_should_cause_warnings,
    with_generated_code_import,
    with_generated_client_fixture,
    with_generated_code_imports,
)


@with_generated_client_fixture(
"""
components:
  schemas:
    MyEnum:
      type: string
      enum: ["a", "B"]
    MyIntEnum:
      type: integer
      enum: [2, 3]
    MyModel:
      properties:
        enumProp: {"$ref": "#/components/schemas/MyEnum"}
        intEnumProp: {"$ref": "#/components/schemas/MyIntEnum"}
        nullableEnumProp:
          oneOf:
            - {"$ref": "#/components/schemas/MyEnum"}
            - type: "null"
""")
@with_generated_code_imports(".models.MyEnum", ".models.MyIntEnum", ".models.MyModel")
class TestEnumClasses:
    def test_enum_classes(self, MyEnum, MyIntEnum):
        assert MyEnum.A == MyEnum("a")
        assert MyEnum.B == MyEnum("B")
        assert MyIntEnum.VALUE_2 == MyIntEnum(2)
        assert MyIntEnum.VALUE_3 == MyIntEnum(3)

    def test_enum_prop(self, MyModel, MyEnum, MyIntEnum):
        assert_model_decode_encode(MyModel, {"enumProp": "B"}, MyModel(enum_prop=MyEnum.B))
        assert_model_decode_encode(MyModel, {"intEnumProp": 2}, MyModel(int_enum_prop=MyIntEnum.VALUE_2))

    def test_enum_prop_type(self, MyModel, MyEnum, MyIntEnum):
        assert isinstance(MyModel.from_dict({"enumProp": "B"}).enum_prop, MyEnum)
        assert isinstance(MyModel.from_dict({"intEnumProp": 2}).int_enum_prop, MyIntEnum)

    def test_nullable_enum_prop(self, MyModel, MyEnum):
        assert_model_decode_encode(
            MyModel,
            {"nullableEnumProp": "B"},
            MyModel(nullable_enum_prop=MyEnum.B),
        )
        assert_model_decode_encode(
            MyModel,
            {"nullableEnumProp": None},
            MyModel(nullable_enum_prop=None),
        )
    
    def test_invalid_values(self, MyModel):
        with pytest.raises(ValueError):
            MyModel.from_dict({"enumProp": "c"})
        with pytest.raises(ValueError):
            MyModel.from_dict({"enumProp": "A"})
        with pytest.raises(ValueError):
            MyModel.from_dict({"enumProp": 2})
        with pytest.raises(ValueError):
            MyModel.from_dict({"intEnumProp": 0})
        with pytest.raises(ValueError):
            MyModel.from_dict({"intEnumProp": "a"})


@with_generated_client_fixture(
"""
components:
  schemas:
    MyEnum:
      type: string
      enum: ["a", "A"]
    MyIntEnum:
      type: integer
      enum: [2, 3]
    MyModel:
      properties:
        enumProp: {"$ref": "#/components/schemas/MyEnum"}
        intEnumProp: {"$ref": "#/components/schemas/MyIntEnum"}
        nullableEnumProp:
          oneOf:
            - {"$ref": "#/components/schemas/MyEnum"}
            - type: "null"
""",
    config="""
literal_enums: true
""",
)
@with_generated_code_import(".models.MyModel")
class TestLiteralEnums:
    def test_enum_prop(self, MyModel):
        assert_model_decode_encode(MyModel, {"enumProp": "a"}, MyModel(enum_prop="a"))
        assert_model_decode_encode(MyModel, {"enumProp": "A"}, MyModel(enum_prop="A"))
        assert_model_decode_encode(MyModel, {"intEnumProp": 2}, MyModel(int_enum_prop=2))

    def test_enum_prop_type(self, MyModel):
        assert MyModel.from_dict({"enumProp": "a"}).enum_prop.__class__ is str
        assert MyModel.from_dict({"intEnumProp": 2}).int_enum_prop.__class__ is int

    def test_nullable_enum_prop(self, MyModel):
        assert_model_decode_encode(
            MyModel,
            {"nullableEnumProp": "a"},
            MyModel(nullable_enum_prop="a"),
        )
        assert_model_decode_encode(
            MyModel,
            {"nullableEnumProp": None},
            MyModel(nullable_enum_prop=None),
        )

    def test_invalid_values(self, MyModel):
        with pytest.raises(TypeError):
            MyModel.from_dict({"enumProp": "c"})
        with pytest.raises(TypeError):
            MyModel.from_dict({"enumProp": 2})
        with pytest.raises(TypeError):
            MyModel.from_dict({"intEnumProp": 0})
        with pytest.raises(TypeError):
            MyModel.from_dict({"intEnumProp": "a"})


@with_generated_client_fixture(
"""
components:
  schemas:
    MyModel:
      properties:
        mustBeErnest:
          const: Ernest
        mustBeThirty:
          const: 30
""",
)
@with_generated_code_import(".models.MyModel")
class TestConst:
    def test_valid_string(self, MyModel):
        assert_model_decode_encode(
            MyModel,
            {"mustBeErnest": "Ernest"},
            MyModel(must_be_ernest="Ernest"),
        )

    def test_valid_int(self, MyModel):
        assert_model_decode_encode(
            MyModel,
            {"mustBeThirty": 30},
            MyModel(must_be_thirty=30),
        )

    def test_invalid_string(self, MyModel):
        with pytest.raises(ValueError):
            MyModel.from_dict({"mustBeErnest": "Jack"})

    def test_invalid_int(self, MyModel):
        with pytest.raises(ValueError):
            MyModel.from_dict({"mustBeThirty": 29})


class TestEnumAndConstInvalidSchemas:
    @pytest.fixture(scope="class")
    def warnings(self):
        return inline_spec_should_cause_warnings(
"""
components:
  schemas:
    WithBadDefaultValue:
      enum: ["A"]
      default: "B"
    WithBadDefaultType:
      enum: ["A"]
      default: 123
    WithMixedTypes:
      enum: ["A", 1]
    WithUnsupportedType:
      enum: [1.4, 1.5]
    DefaultNotMatchingConst:
      const: "aaa"
      default: "bbb"
"""
        )

    def test_enum_bad_default_value(self, warnings):
        assert_bad_schema_warning(warnings, "WithBadDefaultValue", "Value B is not valid")

    def test_enum_bad_default_type(self, warnings):
        assert_bad_schema_warning(warnings, "WithBadDefaultType", "Cannot convert 123 to enum")

    def test_enum_mixed_types(self, warnings):
        assert_bad_schema_warning(warnings, "WithMixedTypes", "Enum values must all be the same type")

    def test_enum_unsupported_type(self, warnings):
        assert_bad_schema_warning(warnings, "WithUnsupportedType", "Unsupported enum type")

    def test_const_default_not_matching(self, warnings):
        assert_bad_schema_warning(warnings, "DefaultNotMatchingConst", "Invalid value for const")
