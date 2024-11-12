import pytest
from end_to_end_tests.end_to_end_test_helpers import (
    assert_bad_schema_warning,
    inline_spec_should_cause_warnings,
)


class TestArrayInvalidSchemas:
    @pytest.fixture(scope="class")
    def warnings(self):
        return inline_spec_should_cause_warnings(
"""
components:
  schemas:
    ArrayWithNoItems:
      type: array
    ArrayWithInvalidItemsRef:
      type: array
      items:
        $ref: "#/components/schemas/DoesntExist"
"""
        )

    def test_no_items(self, warnings):
        assert_bad_schema_warning(warnings, "ArrayWithNoItems", "must have items or prefixItems defined")

    def test_invalid_items_ref(self, warnings):
        assert_bad_schema_warning(warnings, "ArrayWithInvalidItemsRef", "invalid data in items of array")
