from end_to_end_tests.functional_tests.helpers import (
    assert_model_decode_encode,
    assert_model_property_type_hint,
    with_generated_client_fixture,
    with_generated_code_imports,
)


@with_generated_client_fixture(
"""
components:
  schemas:
    SimpleObject:
      type: object
      properties:
        name: {"type": "string"}
    ModelWithArrayOfAny:
      properties:
        arrayProp:
          type: array
          items: {}
    ModelWithArrayOfInts:
      properties:
        arrayProp:
          type: array
          items: {"type": "integer"}
    ModelWithArrayOfObjects:
      properties:
        arrayProp:
          type: array
          items: {"$ref": "#/components/schemas/SimpleObject"}
""")
@with_generated_code_imports(
    ".models.ModelWithArrayOfAny",
    ".models.ModelWithArrayOfInts",
    ".models.ModelWithArrayOfObjects",
    ".models.SimpleObject",
)
class TestArraySchemas:
    def test_array_of_any(self, ModelWithArrayOfAny):
        assert_model_decode_encode(
            ModelWithArrayOfAny,
            {"arrayProp": ["a", 1]},
            ModelWithArrayOfAny(array_prop=["a", 1]),
        )

    def test_array_of_int(self, ModelWithArrayOfInts):
        assert_model_decode_encode(
            ModelWithArrayOfInts,
            {"arrayProp": [1, 2]},
            ModelWithArrayOfInts(array_prop=[1, 2]),
        )

    def test_array_of_object(self, ModelWithArrayOfObjects, SimpleObject):
        assert_model_decode_encode(
            ModelWithArrayOfObjects,
            {"arrayProp": [{"name": "a"}, {"name": "b"}]},
            ModelWithArrayOfObjects(array_prop=[SimpleObject(name="a"), SimpleObject(name="b")]),
        )

    def test_type_hints(self, ModelWithArrayOfAny, ModelWithArrayOfInts, ModelWithArrayOfObjects):
        assert_model_property_type_hint(ModelWithArrayOfAny, "array_prop", "list[Any] | Unset")
        assert_model_property_type_hint(ModelWithArrayOfInts, "array_prop", "list[int] | Unset")
        assert_model_property_type_hint(ModelWithArrayOfObjects, "array_prop", "list[SimpleObject] | Unset")


@with_generated_client_fixture(
"""
components:
  schemas:
    SimpleObject:
      type: object
      properties:
        name: {"type": "string"}
    ModelWithSinglePrefixItem:
      type: object
      properties:
        arrayProp:
          type: array
          prefixItems:
            - type: string
    ModelWithPrefixItems:
      type: object
      properties:
        arrayProp:
          type: array
          prefixItems:
            - $ref: "#/components/schemas/SimpleObject"
            - type: string
    ModelWithMixedItems:
      type: object
      properties:
        arrayProp:
          type: array
          prefixItems:
            - $ref: "#/components/schemas/SimpleObject"
          items:
            type: string
""")
@with_generated_code_imports(
    ".models.ModelWithSinglePrefixItem",
    ".models.ModelWithPrefixItems",
    ".models.ModelWithMixedItems",
    ".models.SimpleObject",
)
class TestArraysWithPrefixItems:
    def test_single_prefix_item(self, ModelWithSinglePrefixItem):
        assert_model_decode_encode(
            ModelWithSinglePrefixItem,
            {"arrayProp": ["a"]},
            ModelWithSinglePrefixItem(array_prop=["a"]),
        )

    def test_prefix_items(self, ModelWithPrefixItems, SimpleObject):
        assert_model_decode_encode(
            ModelWithPrefixItems,
            {"arrayProp": [{"name": "a"}, "b"]},
            ModelWithPrefixItems(array_prop=[SimpleObject(name="a"), "b"]),
        )

    def test_prefix_items_and_regular_items(self, ModelWithMixedItems, SimpleObject):
        assert_model_decode_encode(
            ModelWithMixedItems,
            {"arrayProp": [{"name": "a"}, "b"]},
            ModelWithMixedItems(array_prop=[SimpleObject(name="a"), "b"]),
        )

    def test_type_hints(self, ModelWithSinglePrefixItem, ModelWithPrefixItems, ModelWithMixedItems):
        assert_model_property_type_hint(ModelWithSinglePrefixItem, "array_prop", "list[str] | Unset")
        assert_model_property_type_hint(
            ModelWithPrefixItems,
            "array_prop",
            "list[SimpleObject | str] | Unset",
        )
        assert_model_property_type_hint(
            ModelWithMixedItems,
            "array_prop",
            "list[SimpleObject | str] | Unset",
        )
        # Note, this test is asserting the current behavior which, due to limitations of the implementation
        # (see: https://github.com/openapi-generators/openapi-python-client/pull/1130), is not really doing
        # tuple type validation-- the ordering of prefixItems is ignored, and instead all of the types are
        # simply treated as a union.
