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

    def test_invalid_default(self, generated_client):
        assert_bad_schema(generated_client, "UnionWithInvalidDefault", "Invalid int value: aaa")

    def test_invalid_property(self, generated_client):
        assert_bad_schema(generated_client, "UnionWithMalformedVariant", "Invalid property in union")


@with_generated_client_fixture(
"""
components:
  schemas:
    ModelType1:
      type: object
      properties:
        modelType: {"type": "string"}
        name: {"type": "string"}
      required: ["modelType"]
    ModelType2:
      type: object
      properties:
        modelType: {"type": "string"}
        name: {"type": "string"}
      required: ["modelType"]
    ModelType3:
      type: object
      properties:
        modelType: {"type": "string"}
        name: {"type": "string"}
      required: ["modelType"]
    StringType:
      type: string
    WithUnknownSchemaInMapping:
      type: object
      properties:
        unionProp:
          oneOf:
            - $ref: "#/components/schemas/ModelType1"
            - $ref: "#/components/schemas/ModelType2"
          discriminator:
            propertyName: modelType
            mapping:
              "type1": "#/components/schemas/ModelType1"
              "type2": "#/components/schemas/DoesntExist"
    WithReferenceToSchemaNotInUnion:
      type: object
      properties:
        unionProp:
          oneOf:
            - $ref: "#/components/schemas/ModelType1"
            - $ref: "#/components/schemas/ModelType2"
          discriminator:
            propertyName: modelType
            mapping:
              "type1": "#/components/schemas/ModelType1"
              "type2": "#/components/schemas/ModelType2"
              "type3": "#/components/schemas/ModelType3"
    WithNonObjectVariant:
      type: object
      properties:
        unionProp:
          oneOf:
            - $ref: "#/components/schemas/ModelType1"
            - $ref: "#/components/schemas/StringType"
          discriminator:
            propertyName: modelType
    WithInlineSchema:
      type: object
      properties:
        unionProp:
          oneOf:
            - $ref: "#/components/schemas/ModelType1"
            - type: object
              properties:
                modelType: {"type": "string"}
                name: {"type": "string"}
          discriminator:
            propertyName: modelType
"""    
)
class TestInvalidDiscriminators:
    def test_invalid_reference(self, generated_client):
        assert_bad_schema(
            generated_client,
            "WithUnknownSchemaInMapping",
            'Invalid reference "#/components/schemas/DoesntExist" in discriminator mapping',
        )

    def test_reference_to_schema_not_in_union(self, generated_client):
        assert_bad_schema(
            generated_client,
            "WithReferenceToSchemaNotInUnion",
            'Discriminator mapping referred to "ModelType3" which is not one of the schema variants',
        )

    def test_non_object_variant(self, generated_client):
        assert_bad_schema(
            generated_client,
            "WithNonObjectVariant",
            "All schema variants must be objects when using a discriminator",
        )

    def test_inline_schema(self, generated_client):
        assert_bad_schema(
            generated_client,
            "WithInlineSchema",
            "Inline schema declarations are not allowed when using a discriminator",
        )
