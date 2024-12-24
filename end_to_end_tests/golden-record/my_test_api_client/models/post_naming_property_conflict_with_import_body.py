from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostNamingPropertyConflictWithImportBody")


@_attrs_define
class PostNamingPropertyConflictWithImportBody:
    """
    Attributes:
        field (Union[Unset, str]): A python_name of field should not interfere with attrs field
        define (Union[Unset, str]): A python_name of define should not interfere with attrs define
    """

    field: Union[Unset, str] = UNSET
    define: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field = self.field

        define = self.define

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if field is not UNSET:
            field_dict["Field"] = field
        if define is not UNSET:
            field_dict["Define"] = define

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        field = d.pop("Field", UNSET)

        define = d.pop("Define", UNSET)

        post_naming_property_conflict_with_import_body = cls(
            field=field,
            define=define,
        )

        post_naming_property_conflict_with_import_body.additional_properties = d
        return post_naming_property_conflict_with_import_body

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
