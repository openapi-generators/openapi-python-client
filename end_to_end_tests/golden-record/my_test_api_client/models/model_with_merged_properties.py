import datetime
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.model_with_merged_properties_string_to_enum import ModelWithMergedPropertiesStringToEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelWithMergedProperties")


@_attrs_define
class ModelWithMergedProperties:
    """
    Attributes:
        simple_string (Union[Unset, str]): extended simpleString description Default: 'new default'.
        string_to_enum (Union[Unset, ModelWithMergedPropertiesStringToEnum]):  Default:
            ModelWithMergedPropertiesStringToEnum.A.
        string_to_date (Union[Unset, datetime.date]):
        number_to_int (Union[Unset, int]):
        any_to_string (Union[Unset, str]):  Default: 'x'.
    """

    simple_string: Union[Unset, str] = "new default"
    string_to_enum: Union[Unset, ModelWithMergedPropertiesStringToEnum] = ModelWithMergedPropertiesStringToEnum.A
    string_to_date: Union[Unset, datetime.date] = UNSET
    number_to_int: Union[Unset, int] = UNSET
    any_to_string: Union[Unset, str] = "x"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        simple_string = self.simple_string

        string_to_enum: Union[Unset, str] = UNSET
        if not isinstance(self.string_to_enum, Unset):
            string_to_enum = self.string_to_enum.value

        string_to_date: Union[Unset, str] = UNSET
        if not isinstance(self.string_to_date, Unset):
            string_to_date = self.string_to_date.isoformat()

        number_to_int = self.number_to_int

        any_to_string = self.any_to_string

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if simple_string is not UNSET:
            field_dict["simpleString"] = simple_string
        if string_to_enum is not UNSET:
            field_dict["stringToEnum"] = string_to_enum
        if string_to_date is not UNSET:
            field_dict["stringToDate"] = string_to_date
        if number_to_int is not UNSET:
            field_dict["numberToInt"] = number_to_int
        if any_to_string is not UNSET:
            field_dict["anyToString"] = any_to_string

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        simple_string = d.pop("simpleString", UNSET)

        _string_to_enum = d.pop("stringToEnum", UNSET)
        string_to_enum: Union[Unset, ModelWithMergedPropertiesStringToEnum]
        if isinstance(_string_to_enum, Unset):
            string_to_enum = UNSET
        else:
            string_to_enum = ModelWithMergedPropertiesStringToEnum(_string_to_enum)

        _string_to_date = d.pop("stringToDate", UNSET)
        string_to_date: Union[Unset, datetime.date]
        if isinstance(_string_to_date, Unset):
            string_to_date = UNSET
        else:
            string_to_date = isoparse(_string_to_date).date()

        number_to_int = d.pop("numberToInt", UNSET)

        any_to_string = d.pop("anyToString", UNSET)

        model_with_merged_properties = cls(
            simple_string=simple_string,
            string_to_enum=string_to_enum,
            string_to_date=string_to_date,
            number_to_int=number_to_int,
            any_to_string=any_to_string,
        )

        model_with_merged_properties.additional_properties = d
        return model_with_merged_properties

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
