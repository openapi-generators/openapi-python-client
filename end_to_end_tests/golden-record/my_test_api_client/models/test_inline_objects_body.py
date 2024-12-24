from typing import Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="TestInlineObjectsBody")


@_attrs_define
class TestInlineObjectsBody:
    """
    Attributes:
        a_property (Union[Unset, str]):
    """

    a_property: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        a_property = self.a_property

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if a_property is not UNSET:
            field_dict["a_property"] = a_property

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        a_property = d.pop("a_property", UNSET)

        test_inline_objects_body = cls(
            a_property=a_property,
        )

        return test_inline_objects_body
