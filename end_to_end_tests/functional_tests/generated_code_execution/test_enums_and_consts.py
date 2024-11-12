from typing import Literal, Union
import pytest
from end_to_end_tests.end_to_end_test_helpers import (
    assert_model_decode_encode,
    assert_model_property_type_hint,
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
      enum: ["a", "B", "a23", "123", "1bc", "a Thing WIth spaces", ""]
    MyModel:
      properties:
        enumProp: {"$ref": "#/components/schemas/MyEnum"}
        inlineEnumProp:
          type: string
          enum: ["a", "b"]
    MyModelWithRequired:
      properties:
        enumProp: {"$ref": "#/components/schemas/MyEnum"}
      required: ["enumProp"]
""")
@with_generated_code_imports(
    ".models.MyEnum",
    ".models.MyModel",
    ".models.MyModelInlineEnumProp",
    ".models.MyModelWithRequired",
    ".types.Unset",
)
class TestStringEnumClass:
    @pytest.mark.parametrize(
        "expected_name,expected_value",
        [
            ("A", "a"),
            ("B", "B"),
            ("A23", "a23"),
            ("VALUE_3", "123"),
            ("VALUE_4", "1bc"),
            ("A_THING_WITH_SPACES", "a Thing WIth spaces"),
            ("VALUE_6", ""),
        ],
    )   
    def test_enum_values(self, MyEnum, expected_name, expected_value):
        assert getattr(MyEnum, expected_name) == MyEnum(expected_value)

    def test_enum_prop_in_object(self, MyEnum, MyModel, MyModelInlineEnumProp):
        assert_model_decode_encode(MyModel, {"enumProp": "B"}, MyModel(enum_prop=MyEnum.B))
        assert_model_decode_encode(
            MyModel,
            {"inlineEnumProp": "a"},
            MyModel(inline_enum_prop=MyModelInlineEnumProp.A),
        )

    def test_type_hints(self, MyModel, MyModelWithRequired, MyEnum, Unset):
        optional_type = Union[Unset, MyEnum]
        assert_model_property_type_hint(MyModel,"enum_prop", optional_type)
        assert_model_property_type_hint(MyModelWithRequired, "enum_prop", MyEnum)

    def test_invalid_values(self, MyModel):
        with pytest.raises(ValueError):
            MyModel.from_dict({"enumProp": "c"})
        with pytest.raises(ValueError):
            MyModel.from_dict({"enumProp": "A"})
        with pytest.raises(ValueError):
            MyModel.from_dict({"enumProp": 2})


@with_generated_client_fixture(
"""
components:
  schemas:
    MyEnum:
      type: integer
      enum: [2, 3, -4]
    MyModel:
      properties:
        enumProp: {"$ref": "#/components/schemas/MyEnum"}
        inlineEnumProp:
          type: string
          enum: [2, 3]
    MyModelWithRequired:
      properties:
        enumProp: {"$ref": "#/components/schemas/MyEnum"}
      required: ["enumProp"]
""")
@with_generated_code_imports(
    ".models.MyEnum",
    ".models.MyModel",
    ".models.MyModelInlineEnumProp",
    ".models.MyModelWithRequired",
    ".types.Unset",
)
class TestIntEnumClass:
    @pytest.mark.parametrize(
        "expected_name,expected_value",
        [
            ("VALUE_2", 2),
            ("VALUE_3", 3),
            ("VALUE_NEGATIVE_4", -4),
        ],
    )   
    def test_enum_values(self, MyEnum, expected_name, expected_value):
        assert getattr(MyEnum, expected_name) == MyEnum(expected_value)

    def test_enum_prop_in_object(self, MyEnum, MyModel, MyModelInlineEnumProp):
        assert_model_decode_encode(MyModel, {"enumProp": 2}, MyModel(enum_prop=MyEnum.VALUE_2))
        assert_model_decode_encode(
            MyModel,
            {"inlineEnumProp": 2},
            MyModel(inline_enum_prop=MyModelInlineEnumProp.VALUE_2),
        )

    def test_type_hints(self, MyModel, MyModelWithRequired, MyEnum, Unset):
        optional_type = Union[Unset, MyEnum]
        assert_model_property_type_hint(MyModel,"enum_prop", optional_type)
        assert_model_property_type_hint(MyModelWithRequired, "enum_prop", MyEnum)

    def test_invalid_values(self, MyModel):
        with pytest.raises(ValueError):
            MyModel.from_dict({"enumProp": 5})
        with pytest.raises(ValueError):
            MyModel.from_dict({"enumProp": "a"})


@with_generated_client_fixture(
"""
components:
  schemas:
    MyEnum:
      type: string
      enum: ["a", "b"]
    MyEnumIncludingNull:
      type: ["string", "null"]
      enum: ["a", "b", null]
    MyNullOnlyEnum:
      enum: [null]
    MyModel:
      properties:
        nullableEnumProp:
          oneOf:
            - {"$ref": "#/components/schemas/MyEnum"}
            - type: "null"
        enumIncludingNullProp: {"$ref": "#/components/schemas/MyEnumIncludingNull"}
        nullOnlyEnumProp: {"$ref": "#/components/schemas/MyNullOnlyEnum"}
""")
@with_generated_code_imports(
    ".models.MyEnum",
    ".models.MyEnumIncludingNullType1", # see comment in test_nullable_enum_prop
    ".models.MyModel",
    ".types.Unset",
)
class TestNullableEnums:
    def test_nullable_enum_prop(self, MyModel, MyEnum, MyEnumIncludingNullType1):
        # Note, MyEnumIncludingNullType1 should be named just MyEnumIncludingNull -
        # known bug: https://github.com/openapi-generators/openapi-python-client/issues/1120
        assert_model_decode_encode(MyModel, {"nullableEnumProp": "b"}, MyModel(nullable_enum_prop=MyEnum.B))
        assert_model_decode_encode(MyModel, {"nullableEnumProp": None}, MyModel(nullable_enum_prop=None))
        assert_model_decode_encode(
            MyModel,
            {"enumIncludingNullProp": "a"},
            MyModel(enum_including_null_prop=MyEnumIncludingNullType1.A),
        )
        assert_model_decode_encode( MyModel, {"enumIncludingNullProp": None}, MyModel(enum_including_null_prop=None))
        assert_model_decode_encode(MyModel, {"nullOnlyEnumProp": None}, MyModel(null_only_enum_prop=None))
    
    def test_type_hints(self, MyModel, MyEnum, Unset):
        expected_type = Union[MyEnum, None, Unset]
        assert_model_property_type_hint(MyModel, "nullable_enum_prop", expected_type)
    

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


# The following tests of literal enums use basically the same specs as the tests above, but
# the "literal_enums" option is enabled in the test configuration.

@with_generated_client_fixture(
"""
components:
  schemas:
    MyEnum:
      type: string
      enum: ["a", "A", "b"]
    MyModel:
      properties:
        enumProp: {"$ref": "#/components/schemas/MyEnum"}
        inlineEnumProp:
          type: string
          enum: ["a", "b"]
    MyModelWithRequired:
      properties:
        enumProp: {"$ref": "#/components/schemas/MyEnum"}
      required: ["enumProp"]
""",
    config="literal_enums: true",
)
@with_generated_code_imports(
    ".models.MyModel",
    ".models.MyModelWithRequired",
    ".types.Unset",
)
class TestStringLiteralEnum:
    def test_enum_prop(self, MyModel):
        assert_model_decode_encode(MyModel, {"enumProp": "a"}, MyModel(enum_prop="a"))
        assert_model_decode_encode(MyModel, {"enumProp": "A"}, MyModel(enum_prop="A"))
        assert_model_decode_encode(MyModel, {"inlineEnumProp": "a"}, MyModel(inline_enum_prop="a"))
    
    def test_type_hints(self, MyModel, MyModelWithRequired, Unset):
        literal_type = Literal["a", "A", "b"]
        optional_type = Union[Unset, literal_type]
        assert_model_property_type_hint(MyModel, "enum_prop", optional_type)
        assert_model_property_type_hint(MyModelWithRequired, "enum_prop", literal_type)

    def test_invalid_values(self, MyModel):
        with pytest.raises(TypeError):
            MyModel.from_dict({"enumProp": "c"})
        with pytest.raises(TypeError):
            MyModel.from_dict({"enumProp": 2})


@with_generated_client_fixture(
"""
components:
  schemas:
    MyEnum:
      type: integer
      enum: [2, 3, -4]
    MyModel:
      properties:
        enumProp: {"$ref": "#/components/schemas/MyEnum"}
        inlineEnumProp:
          type: string
          enum: [2, 3]
    MyModelWithRequired:
      properties:
        enumProp: {"$ref": "#/components/schemas/MyEnum"}
      required: ["enumProp"]
""",
    config="literal_enums: true",
)
@with_generated_code_imports(
    ".models.MyModel",
    ".models.MyModelWithRequired",
    ".types.Unset",
)
class TestIntLiteralEnum:
    def test_enum_prop(self, MyModel):
        assert_model_decode_encode(MyModel, {"enumProp": 2}, MyModel(enum_prop=2))
        assert_model_decode_encode(MyModel, {"enumProp": -4}, MyModel(enum_prop=-4))
        assert_model_decode_encode(MyModel, {"inlineEnumProp": 2}, MyModel(inline_enum_prop=2))
    
    def test_type_hints(self, MyModel, MyModelWithRequired, Unset):
        literal_type = Literal[2, 3, -4]
        optional_type = Union[Unset, literal_type]
        assert_model_property_type_hint(MyModel, "enum_prop", optional_type)
        assert_model_property_type_hint(MyModelWithRequired, "enum_prop", literal_type)

    def test_invalid_values(self, MyModel):
        with pytest.raises(TypeError):
            MyModel.from_dict({"enumProp": 4})
        with pytest.raises(TypeError):
            MyModel.from_dict({"enumProp": "a"})


@with_generated_client_fixture(
"""
components:
  schemas:
    MyEnum:
      type: string
      enum: ["a", "A"]
    MyEnumIncludingNull:
      type: ["string", "null"]
      enum: ["a", "b", null]
    MyNullOnlyEnum:
      enum: [null]
    MyModel:
      properties:
        enumProp: {"$ref": "#/components/schemas/MyEnum"}
        nullableEnumProp:
          oneOf:
            - {"$ref": "#/components/schemas/MyEnum"}
            - type: "null"
        enumIncludingNullProp: {"$ref": "#/components/schemas/MyEnumIncludingNull"}
        nullOnlyEnumProp: {"$ref": "#/components/schemas/MyNullOnlyEnum"}
""",
    config="literal_enums: true",
)
@with_generated_code_import(".models.MyModel")
class TestNullableLiteralEnum:
    def test_nullable_enum_prop(self, MyModel):
        assert_model_decode_encode(MyModel, {"nullableEnumProp": "B"}, MyModel(nullable_enum_prop="B"))
        assert_model_decode_encode(MyModel, {"nullableEnumProp": None}, MyModel(nullable_enum_prop=None))
        assert_model_decode_encode(MyModel, {"enumIncludingNullProp": "a"}, MyModel(enum_including_null_prop="a"))
        assert_model_decode_encode(MyModel, {"enumIncludingNullProp": None}, MyModel(enum_including_null_prop=None))
        assert_model_decode_encode(MyModel, {"nullOnlyEnumProp": None}, MyModel(null_only_enum_prop=None))
