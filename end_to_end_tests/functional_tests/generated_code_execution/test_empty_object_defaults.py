from end_to_end_tests.functional_tests.helpers import (
    with_generated_client_fixture,
    with_generated_code_imports,
)


@with_generated_client_fixture(
    """
components:
  schemas:
    Holder:
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
@with_generated_code_imports(".models.Holder", ".types.UNSET")
class TestEmptyObjectDefaultOnAUnionMember:
    """An empty object default on a union member leaves the enclosing schema in place. The property generates
    with no default."""

    def test_model_generates_without_the_default(self, Holder, UNSET):
        assert Holder().extras is UNSET

    def test_explicit_value_is_kept(self, Holder):
        assert Holder.from_dict({"extras": {"a": 1}}).to_dict() == {"extras": {"a": 1}}


@with_generated_client_fixture(
    """
components:
  schemas:
    Free:
      type: object
      additionalProperties: true
    Holder:
      type: object
      properties:
        extras:
          allOf:
            - $ref: "#/components/schemas/Free"
          default: {}
"""
)
@with_generated_code_imports(".models.Holder", ".types.UNSET")
class TestEmptyObjectDefaultOnAReferencedModel:
    """The same holds when the model carrying the default is referenced through an ``allOf``."""

    def test_model_generates_without_the_default(self, Holder, UNSET):
        assert Holder().extras is UNSET
