from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.all_of_sub_model_type_enum import AllOfSubModelTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="AllOfSubModel")


@_attrs_define
class AllOfSubModel:
    """
    Attributes:
        a_sub_property (Union[Unset, str]):
        type_ (Union[Unset, str]):
        type_enum (Union[Unset, AllOfSubModelTypeEnum]):
    """

    a_sub_property: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    type_enum: Union[Unset, AllOfSubModelTypeEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        a_sub_property = self.a_sub_property

        type_ = self.type_

        type_enum: Union[Unset, int] = UNSET
        if not isinstance(self.type_enum, Unset):
            type_enum = self.type_enum.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if a_sub_property is not UNSET:
            field_dict["a_sub_property"] = a_sub_property
        if type_ is not UNSET:
            field_dict["type"] = type_
        if type_enum is not UNSET:
            field_dict["type_enum"] = type_enum

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        a_sub_property = d.pop("a_sub_property", UNSET)

        type_ = d.pop("type", UNSET)

        _type_enum = d.pop("type_enum", UNSET)
        type_enum: Union[Unset, AllOfSubModelTypeEnum]
        if isinstance(_type_enum, Unset):
            type_enum = UNSET
        else:
            type_enum = AllOfSubModelTypeEnum(_type_enum)

        all_of_sub_model = cls(
            a_sub_property=a_sub_property,
            type_=type_,
            type_enum=type_enum,
        )

        all_of_sub_model.additional_properties = d
        return all_of_sub_model

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
