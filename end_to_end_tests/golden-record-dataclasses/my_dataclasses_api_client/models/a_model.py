from dataclasses import dataclass as _dataclass
from dataclasses import field as _dataclasses_field
from typing import Any, Dict, List, Type, TypeVar, Union

from ..types import UNSET, Unset

T = TypeVar("T", bound="AModel")


@_dataclass
class AModel:
    """
    Attributes:
        required_string (str):
        optional_string (Union[Unset, str]):
        string_with_default (Union[Unset, str]):  Default: 'abc'.
    """

    required_string: str
    optional_string: Union[Unset, str] = UNSET
    string_with_default: Union[Unset, str] = "abc"
    additional_properties: Dict[str, Any] = _dataclasses_field(init=False, default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        required_string = self.required_string

        optional_string = self.optional_string

        string_with_default = self.string_with_default

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "requiredString": required_string,
            }
        )
        if optional_string is not UNSET:
            field_dict["optionalString"] = optional_string
        if string_with_default is not UNSET:
            field_dict["stringWithDefault"] = string_with_default

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        required_string = d.pop("requiredString")

        optional_string = d.pop("optionalString", UNSET)

        string_with_default = d.pop("stringWithDefault", UNSET)

        a_model = cls(
            required_string=required_string,
            optional_string=optional_string,
            string_with_default=string_with_default,
        )

        a_model.additional_properties = d
        return a_model

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
