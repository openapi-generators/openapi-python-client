import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

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
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        prop1 = self.simple_string
        prop2: Union[Unset, str] = UNSET
        if not isinstance(self.string_to_enum, Unset):
            prop2 = self.string_to_enum.value

        prop3: Union[Unset, str] = UNSET
        if not isinstance(self.string_to_date, Unset):
            prop3 = self.string_to_date.isoformat()
        prop4 = self.number_to_int
        prop5 = self.any_to_string

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict = {
            **field_dict,
            **({} if prop1 is UNSET else {"simpleString": prop1}),
            **({} if prop2 is UNSET else {"stringToEnum": prop2}),
            **({} if prop3 is UNSET else {"stringToDate": prop3}),
            **({} if prop4 is UNSET else {"numberToInt": prop4}),
            **({} if prop5 is UNSET else {"anyToString": prop5}),
        }

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
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
