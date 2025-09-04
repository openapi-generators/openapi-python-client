import pytest

from end_to_end_tests.functional_tests.helpers import assert_bad_schema, with_generated_client_fixture


@with_generated_client_fixture(
    """
components:
  schemas:
    MyModel:
      type: object
      properties:
        booleanProp: {"type": "boolean"}
        stringProp: {"type": "string"}
        numberProp: {"type": "number"}
        intProp: {"type": "integer"}
        anyObjectProp: {"$ref": "#/components/schemas/AnyObject"}
        nullProp: {"type": "null"}
        anyProp: {}
    AnyObject:
      $ref: "#/components/schemas/OtherObject"
    OtherObject:
      $ref: "#/components/schemas/AnyObject"
    
"""
)
class TestReferenceSchemaProperties:
    def test_decode_encode(self, generated_client):
        assert "Circular schema references found" in generated_client.generator_result.stdout
