from end_to_end_tests.functional_tests.helpers import assert_bad_schema, with_generated_client_fixture


@with_generated_client_fixture(
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
class TestUnionInvalidSchemas:
    def test_invalid_reference(self, generated_client):
        assert_bad_schema(generated_client, "UnionWithInvalidReference", "Could not find reference")

    def test_invalid_default(self, generated_client):
        assert_bad_schema(generated_client, "UnionWithInvalidDefault", "Invalid int value: aaa")

    def test_invalid_property(self, generated_client):
        assert_bad_schema(generated_client, "UnionWithMalformedVariant", "Invalid property in union")
