from typing import Any
import pytest
from end_to_end_tests.end_to_end_test_helpers import (
    assert_bad_schema_warning,
    assert_model_decode_encode,
    inline_spec_should_cause_warnings,
    inline_spec_should_fail,
    with_generated_code_import,
    with_generated_client_fixture,
)

# This is a separate file from test_enum_and_const.py because literal enums are not generated
# in the default configuration.


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
    MyEnumIncludingNull:
      type: ["string", "null"]
      enum: ["a", "b", null]
    MyNullOnlyEnum:
      enum: [null]
    MyModel:
      properties:
        enumProp: {"$ref": "#/components/schemas/MyEnum"}
        intEnumProp: {"$ref": "#/components/schemas/MyIntEnum"}
        nullableEnumProp:
          oneOf:
            - {"$ref": "#/components/schemas/MyEnum"}
            - type: "null"
        enumIncludingNullProp: {"$ref": "#/components/schemas/MyEnumIncludingNull"}
        nullOnlyEnumProp: {"$ref": "#/components/schemas/MyNullOnlyEnum"}
        inlineEnumProp:
          type: string
          enum: ["a", "b"]
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
        assert_model_decode_encode(MyModel, {"inlineEnumProp": "a"}, MyModel(inline_enum_prop="a"))

    def test_enum_prop_type(self, MyModel):
        assert MyModel.from_dict({"enumProp": "a"}).enum_prop.__class__ is str
        assert MyModel.from_dict({"intEnumProp": 2}).int_enum_prop.__class__ is int

    def test_nullable_enum_prop(self, MyModel):
        assert_model_decode_encode(MyModel, {"nullableEnumProp": "B"}, MyModel(nullable_enum_prop="B"))
        assert_model_decode_encode(MyModel, {"nullableEnumProp": None}, MyModel(nullable_enum_prop=None))
        assert_model_decode_encode(MyModel, {"enumIncludingNullProp": "a"}, MyModel(enum_including_null_prop="a"))
        assert_model_decode_encode(MyModel, {"enumIncludingNullProp": None}, MyModel(enum_including_null_prop=None))
        assert_model_decode_encode(MyModel, {"nullOnlyEnumProp": None}, MyModel(null_only_enum_prop=None))

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
    MyEnum:
      type: string
      enum: ["a", "A"]
    MyModel:
      properties:
        enumProp:
          allOf:
            - $ref: "#/components/schemas/MyEnum"
          default: A
""",
    config="literal_enums: true",
)
@with_generated_code_import(".models.MyModel")
class TestLiteralEnumDefaults:
    def test_default_value(self, MyModel):
        assert MyModel().enum_prop == "A"


class TestLiteralEnumInvalidSchemas:
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
""",
    config="literal_enums: true",
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

    def test_enum_duplicate_values(self):
        # This one currently causes a full generator failure rather than a warning
        result = inline_spec_should_fail(
"""
components:
  schemas:
    WithDuplicateValues:
      enum: ["x", "x"]
"""
        )
        assert "Duplicate key X in enum" in str(result.exception)
