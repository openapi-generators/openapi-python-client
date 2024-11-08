
from typing import Any
import pytest
from end_to_end_tests.end_to_end_test_helpers import (
    assert_bad_schema_warning,
    assert_model_decode_encode,
    inline_spec_should_cause_warnings,
    inline_spec_should_fail,
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
      enum: ["a", "B", "~weirdstring"]
    MyIntEnum:
      type: integer
      enum: [2, 3, -4]
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
""")
@with_generated_code_imports(
    ".models.MyEnum",
    ".models.MyIntEnum",
    ".models.MyEnumIncludingNullType1", # see comment in test_nullable_enum_prop
    ".models.MyModel",
    ".models.MyModelInlineEnumProp",
)
class TestEnumClasses:
    def test_enum_classes(self, MyEnum, MyIntEnum):
        assert MyEnum.A == MyEnum("a")
        assert MyEnum.B == MyEnum("B")
        assert MyEnum.VALUE_2 == MyEnum("~weirdstring")
        assert MyIntEnum.VALUE_2 == MyIntEnum(2)
        assert MyIntEnum.VALUE_3 == MyIntEnum(3)
        assert MyIntEnum.VALUE_NEGATIVE_4 == MyIntEnum(-4)

    def test_enum_prop(self, MyModel, MyEnum, MyIntEnum, MyModelInlineEnumProp):
        assert_model_decode_encode(MyModel, {"enumProp": "B"}, MyModel(enum_prop=MyEnum.B))
        assert_model_decode_encode(MyModel, {"intEnumProp": 2}, MyModel(int_enum_prop=MyIntEnum.VALUE_2))
        assert_model_decode_encode(
            MyModel,
            {"inlineEnumProp": "a"},
            MyModel(inline_enum_prop=MyModelInlineEnumProp.A),
        )

    def test_enum_prop_type(self, MyModel, MyEnum):
        # Just verifying that it's not using a literal vaue
        assert isinstance(MyModel.from_dict({"enumProp": "B"}).enum_prop, MyEnum)

    def test_nullable_enum_prop(self, MyModel, MyEnum, MyEnumIncludingNullType1):
        # Note, MyEnumIncludingNullType1 should be named just MyEnumIncludingNull -
        # known bug: https://github.com/openapi-generators/openapi-python-client/issues/1120
        assert_model_decode_encode(MyModel, {"nullableEnumProp": "B"}, MyModel(nullable_enum_prop=MyEnum.B))
        assert_model_decode_encode(MyModel, {"nullableEnumProp": None}, MyModel(nullable_enum_prop=None))
        assert_model_decode_encode(
            MyModel,
            {"enumIncludingNullProp": "a"},
            MyModel(enum_including_null_prop=MyEnumIncludingNullType1.A),
        )
        assert_model_decode_encode( MyModel, {"enumIncludingNullProp": None}, MyModel(enum_including_null_prop=None))
        assert_model_decode_encode(MyModel, {"nullOnlyEnumProp": None}, MyModel(null_only_enum_prop=None))
    
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
