from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.an_enum import AnEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="AModelWithOptionalPropertyRefAndDefaultValue")


@_attrs_define
class AModelWithOptionalPropertyRefAndDefaultValue:
    """
    Attributes:
        enum_property_ref (Union[Unset, AnEnum]): For testing Enums in all the ways they can be used  Default:
            AnEnum.FIRST_VALUE.
    """

    enum_property_ref: Union[Unset, AnEnum] = AnEnum.FIRST_VALUE
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        enum_property_ref: Union[Unset, str] = UNSET
        if not isinstance(self.enum_property_ref, Unset):
            enum_property_ref = self.enum_property_ref.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if enum_property_ref is not UNSET:
            field_dict["enum_property_ref"] = enum_property_ref

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        _enum_property_ref = d.pop("enum_property_ref", UNSET)
        enum_property_ref: Union[Unset, AnEnum]
        if isinstance(_enum_property_ref, Unset):
            enum_property_ref = UNSET
        else:
            enum_property_ref = AnEnum(_enum_property_ref)

        a_model_with_optional_property_ref_and_default_value = cls(
            enum_property_ref=enum_property_ref,
        )

        a_model_with_optional_property_ref_and_default_value.additional_properties = d
        return a_model_with_optional_property_ref_and_default_value

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
