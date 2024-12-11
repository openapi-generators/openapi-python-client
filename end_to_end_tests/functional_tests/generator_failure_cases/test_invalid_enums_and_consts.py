from end_to_end_tests.functional_tests.helpers import (
    assert_bad_schema,
    inline_spec_should_fail,
    with_generated_client_fixture,
)


@with_generated_client_fixture(
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
    WithConflictingInlineNames:
      type: object
      properties:
        "12":
          enum: ["a", "b"]
    WithConflictingInlineNames1:
      type: object
      properties:
        "2":
          enum: ["c", "d"]
"""    
)
class TestEnumAndConstInvalidSchemas:
    def test_enum_bad_default_value(self, generated_client):
        assert_bad_schema(generated_client, "WithBadDefaultValue", "Value B is not valid")

    def test_enum_bad_default_type(self, generated_client):
        assert_bad_schema(generated_client, "WithBadDefaultType", "Cannot convert 123 to enum")

    def test_enum_mixed_types(self, generated_client):
        assert_bad_schema(generated_client, "WithMixedTypes", "Enum values must all be the same type")

    def test_enum_unsupported_type(self, generated_client):
        assert_bad_schema(generated_client, "WithUnsupportedType", "Unsupported enum type")

    def test_const_default_not_matching(self, generated_client):
        assert_bad_schema(generated_client, "DefaultNotMatchingConst", "Invalid value for const")

    def test_conflicting_inline_class_names(self, generated_client):
        assert "Found conflicting enums named WithConflictingInlineNames12 with incompatible values" in generated_client.generator_result.output

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


@with_generated_client_fixture(
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
    WithConflictingInlineNames:
      type: object
      properties:
        "12":
          enum: ["a", "b"]
    WithConflictingInlineNames1:
      type: object
      properties:
        "2":
          enum: ["c", "d"]
""",
    config="literal_enums: true",    
)
class TestLiteralEnumInvalidSchemas:
    def test_literal_enum_bad_default_value(self, generated_client):
        assert_bad_schema(generated_client, "WithBadDefaultValue", "Value B is not valid")

    def test_literal_enum_bad_default_type(self, generated_client):
        assert_bad_schema(generated_client, "WithBadDefaultType", "Cannot convert 123 to enum")

    def test_literal_enum_mixed_types(self, generated_client):
        assert_bad_schema(generated_client, "WithMixedTypes", "Enum values must all be the same type")

    def test_literal_enum_unsupported_type(self, generated_client):
        assert_bad_schema(generated_client, "WithUnsupportedType", "Unsupported enum type")

    def test_const_default_not_matching(self, generated_client):
        assert_bad_schema(generated_client, "DefaultNotMatchingConst", "Invalid value for const")

    def test_conflicting_inline_literal_enum_names(self, generated_client):
        assert "Found conflicting enums named WithConflictingInlineNames12 with incompatible values" in generated_client.generator_result.output

    def test_literal_enum_duplicate_values(self):
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
