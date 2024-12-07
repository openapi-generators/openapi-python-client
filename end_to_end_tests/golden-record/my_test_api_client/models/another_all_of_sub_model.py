from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.another_all_of_sub_model_type import AnotherAllOfSubModelType
from ..models.another_all_of_sub_model_type_enum import AnotherAllOfSubModelTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="AnotherAllOfSubModel")


@_attrs_define
class AnotherAllOfSubModel:
    """
    Attributes:
        another_sub_property (Union[Unset, str]):
        type_ (Union[Unset, AnotherAllOfSubModelType]):
        type_enum (Union[Unset, AnotherAllOfSubModelTypeEnum]):
    """

    another_sub_property: Union[Unset, str] = UNSET
    type_: Union[Unset, AnotherAllOfSubModelType] = UNSET
    type_enum: Union[Unset, AnotherAllOfSubModelTypeEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        another_sub_property = self.another_sub_property

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        type_enum: Union[Unset, int] = UNSET
        if not isinstance(self.type_enum, Unset):
            type_enum = self.type_enum.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if another_sub_property is not UNSET:
            field_dict["another_sub_property"] = another_sub_property
        if type_ is not UNSET:
            field_dict["type"] = type_
        if type_enum is not UNSET:
            field_dict["type_enum"] = type_enum

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        another_sub_property = d.pop("another_sub_property", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, AnotherAllOfSubModelType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = AnotherAllOfSubModelType(_type_)

        _type_enum = d.pop("type_enum", UNSET)
        type_enum: Union[Unset, AnotherAllOfSubModelTypeEnum]
        if isinstance(_type_enum, Unset):
            type_enum = UNSET
        else:
            type_enum = AnotherAllOfSubModelTypeEnum(_type_enum)

        another_all_of_sub_model = cls(
            another_sub_property=another_sub_property,
            type_=type_,
            type_enum=type_enum,
        )

        another_all_of_sub_model.additional_properties = d
        return another_all_of_sub_model

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
