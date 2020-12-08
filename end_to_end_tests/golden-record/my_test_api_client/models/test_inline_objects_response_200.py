from typing import Any, Dict, Union

import attr

from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class TestInlineObjectsResponse_200:
    """  """

    a_property: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        a_property = self.a_property

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if a_property is not UNSET:
            field_dict["a_property"] = a_property

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "TestInlineObjectsResponse_200":
        d = src_dict.copy()
        a_property = d.pop("a_property", UNSET)

        test_inline_objects_response_200 = TestInlineObjectsResponse_200(
            a_property=a_property,
        )

        return test_inline_objects_response_200
