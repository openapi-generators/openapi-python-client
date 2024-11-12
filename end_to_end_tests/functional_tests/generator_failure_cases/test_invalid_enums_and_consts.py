import pytest
from end_to_end_tests.end_to_end_test_helpers import (
    assert_bad_schema_warning,
    inline_spec_should_cause_warnings,
    inline_spec_should_fail,
)

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

    def test_conflicting_inline_class_names(self, warnings):
        assert "Found conflicting enums named WithConflictingInlineNames12 with incompatible values" in warnings

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

    def test_literal_enum_bad_default_value(self, warnings):
        assert_bad_schema_warning(warnings, "WithBadDefaultValue", "Value B is not valid")

    def test_literal_enum_bad_default_type(self, warnings):
        assert_bad_schema_warning(warnings, "WithBadDefaultType", "Cannot convert 123 to enum")

    def test_literal_enum_mixed_types(self, warnings):
        assert_bad_schema_warning(warnings, "WithMixedTypes", "Enum values must all be the same type")

    def test_literal_enum_unsupported_type(self, warnings):
        assert_bad_schema_warning(warnings, "WithUnsupportedType", "Unsupported enum type")

    def test_const_default_not_matching(self, warnings):
        assert_bad_schema_warning(warnings, "DefaultNotMatchingConst", "Invalid value for const")

    def test_conflicting_inline_literal_enum_names(self, warnings):
        assert "Found conflicting enums named WithConflictingInlineNames12 with incompatible values" in warnings

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
