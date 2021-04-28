from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="TestInlineObjectsResponse200")


@attr.s(auto_attribs=True)
class TestInlineObjectsResponse200:
    """ """

    a_property: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        a_property = self.a_property

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if a_property is not UNSET:
            field_dict["a_property"] = a_property

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        a_property = d.pop("a_property", UNSET)

        test_inline_objects_response_200 = cls(
            a_property=a_property,
        )

        return test_inline_objects_response_200
