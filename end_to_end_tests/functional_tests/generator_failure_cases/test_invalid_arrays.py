import pytest

from end_to_end_tests.functional_tests.helpers import assert_bad_schema, with_generated_client_fixture


@with_generated_client_fixture(
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
class TestArrayInvalidSchemas:
    def test_no_items(self, generated_client):
        assert_bad_schema(generated_client, "ArrayWithNoItems", "must have items or prefixItems defined")

    def test_invalid_items_ref(self, generated_client):
        assert_bad_schema(generated_client, "ArrayWithInvalidItemsRef", "invalid data in items of array")
