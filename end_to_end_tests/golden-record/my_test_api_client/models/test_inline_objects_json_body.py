from typing import Any, Dict, Union

import attr

from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class TestInlineObjectsJsonBody:
    """  """

    a_property: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        a_property = self.a_property

        field_dict = {}
        if a_property is not UNSET:
            field_dict["a_property"] = a_property

        return field_dict

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "TestInlineObjectsJsonBody":
        a_property = d.get("a_property", UNSET)

        return TestInlineObjectsJsonBody(
            a_property=a_property,
        )
