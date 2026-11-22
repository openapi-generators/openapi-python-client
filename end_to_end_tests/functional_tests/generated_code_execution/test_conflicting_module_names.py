from end_to_end_tests.functional_tests.helpers import (
    assert_model_decode_encode,
    with_generated_client_fixture,
    with_generated_code_imports,
)


@with_generated_client_fixture(
    """
components:
  schemas:
    VLAN:
      type: object
      properties:
        vlanId: {"type": "integer"}
      required: ["vlanId"]
    Vlan:
      type: object
      properties:
        name: {"type": "string"}
      required: ["name"]
    Container:
      type: object
      properties:
        upper: {"$ref": "#/components/schemas/VLAN"}
        lower: {"$ref": "#/components/schemas/Vlan"}
      required: ["upper", "lower"]
"""
)
@with_generated_code_imports(
    ".models.VLAN",
    ".models.Vlan",
    ".models.Container",
)
class TestConflictingModuleNames:
    def test_both_models_are_generated(self, VLAN, Vlan, Container):
        assert_model_decode_encode(VLAN, {"vlanId": 1}, VLAN(vlan_id=1))
        assert_model_decode_encode(Vlan, {"name": "a"}, Vlan(name="a"))
        assert_model_decode_encode(
            Container,
            {"upper": {"vlanId": 1}, "lower": {"name": "a"}},
            Container(upper=VLAN(vlan_id=1), lower=Vlan(name="a")),
        )
