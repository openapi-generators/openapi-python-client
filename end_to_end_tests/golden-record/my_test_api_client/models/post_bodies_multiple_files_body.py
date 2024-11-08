from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostBodiesMultipleFilesBody")


@_attrs_define
class PostBodiesMultipleFilesBody:
    """
    Attributes:
        a (Union[Unset, str]):
    """

    a: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        prop1 = self.a

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict = {
            **field_dict,
            **({} if prop1 is UNSET else {"a": prop1}),
        }

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        prop1 = self.a if isinstance(self.a, Unset) else (None, str(self.a).encode(), "text/plain")

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict = {
            **field_dict,
            **({} if prop1 is UNSET else {"a": prop1}),
        }

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        a = d.pop("a", UNSET)

        post_bodies_multiple_files_body = cls(
            a=a,
        )

        post_bodies_multiple_files_body.additional_properties = d
        return post_bodies_multiple_files_body

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
