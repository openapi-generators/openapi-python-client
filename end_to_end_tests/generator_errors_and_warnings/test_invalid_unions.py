import pytest
from end_to_end_tests.end_to_end_test_helpers import (
    assert_bad_schema_warning,
    inline_spec_should_cause_warnings,
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
    UnionWithMalformedVariant:
      anyOf:
        - type: string
        - type: array  # invalid because no items
"""
        )

    def test_invalid_reference(self, warnings):
        assert_bad_schema_warning(warnings, "UnionWithInvalidReference", "Could not find reference")

    def test_invalid_default(self, warnings):
        assert_bad_schema_warning(warnings, "UnionWithInvalidDefault", "Invalid int value: aaa")

    def test_invalid_property(self, warnings):
        assert_bad_schema_warning(warnings, "UnionWithMalformedVariant", "Invalid property in union")