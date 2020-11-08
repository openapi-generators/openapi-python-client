from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class TestInlineObjectsjsonBody:
    """  """

    a_property: str

    def to_dict(self) -> Dict[str, Any]:
        a_property = self.a_property

        field_dict = {
            "a_property": a_property,
        }

        return field_dict

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "TestInlineObjectsjsonBody":
        a_property = d["a_property"]

        return TestInlineObjectsjsonBody(
            a_property=a_property,
        )
