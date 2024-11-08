from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="TestInlineObjectsResponse200")


@_attrs_define
class TestInlineObjectsResponse200:
    """
    Attributes:
        a_property (Union[Unset, str]):
    """

    a_property: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        prop1 = self.a_property

        field_dict: Dict[str, Any] = {}
        field_dict = {
            **field_dict,
            **({} if prop1 is UNSET else {"a_property": prop1}),
        }

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        a_property = d.pop("a_property", UNSET)

        test_inline_objects_response_200 = cls(
            a_property=a_property,
        )

        return test_inline_objects_response_200
