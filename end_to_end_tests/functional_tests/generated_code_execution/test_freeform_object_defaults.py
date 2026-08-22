from end_to_end_tests.functional_tests.helpers import (
    with_generated_client_fixture,
    with_generated_code_imports,
)


@with_generated_client_fixture(
"""
components:
  schemas:
    ModelWithFreeformDefault:
      type: object
      properties:
        extras:
          anyOf:
            - type: object
              additionalProperties: true
            - type: "null"
          default: {}
"""
)
@with_generated_code_imports(".models.ModelWithFreeformDefault")
class TestFreeformObjectDefault:
    """A freeform object (``type: object`` with ``additionalProperties: true`` and no
    declared properties) inside a union with ``default: {}`` should generate a model
    whose default initializer constructs the empty inner container.
    """

    def test_default_is_constructed(self, ModelWithFreeformDefault):
        instance = ModelWithFreeformDefault()
        assert instance.extras.additional_properties == {}

    def test_explicit_value_overrides_default(self, ModelWithFreeformDefault):
        inner_type = type(ModelWithFreeformDefault().extras)
        custom = inner_type.from_dict({"a": 1})
        instance = ModelWithFreeformDefault(extras=custom)
        assert instance.to_dict() == {"extras": {"a": 1}}
