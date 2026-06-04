from end_to_end_tests.functional_tests.helpers import (
    with_generated_client_fixture,
    with_generated_code_imports,
)


@with_generated_client_fixture(
"""
components:
  schemas:
    Thing-Input:
      title: Thing
      type: object
      properties:
        name: {"type": "string"}
    Thing-Output:
      title: Thing
      type: object
      properties:
        name: {"type": "string"}
        id: {"type": "string"}
"""
)
@with_generated_code_imports(".models.Thing", ".models.ThingOutput")
class TestCollidingTitlesFallBackToSchemaKey:
    """FastAPI emits the same ``title`` for input and output variants of a model
    (for example ``Thing-Input`` and ``Thing-Output`` both carrying ``title: Thing``).
    The first variant takes the title-derived class name, and the second falls back
    to its schema key so both schemas survive.
    """

    def test_first_variant_uses_title(self, Thing):
        assert Thing.__name__ == "Thing"
        instance = Thing(name="x")
        assert instance.to_dict() == {"name": "x"}

    def test_second_variant_uses_schema_key(self, ThingOutput):
        assert ThingOutput.__name__ == "ThingOutput"
        instance = ThingOutput(name="x", id="123")
        assert instance.to_dict() == {"name": "x", "id": "123"}
