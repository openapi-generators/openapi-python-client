from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelWithNoDescription")


@_attrs_define
class ModelWithNoDescription:
    prop_with_no_desc: Union[Unset, str] = UNSET
    prop_with_desc: Union[Unset, str] = UNSET
    """ This is a nice property. """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        prop_with_no_desc = self.prop_with_no_desc

        prop_with_desc = self.prop_with_desc

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if prop_with_no_desc is not UNSET:
            field_dict["propWithNoDesc"] = prop_with_no_desc
        if prop_with_desc is not UNSET:
            field_dict["propWithDesc"] = prop_with_desc

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        prop_with_no_desc = d.pop("propWithNoDesc", UNSET)

        prop_with_desc = d.pop("propWithDesc", UNSET)

        model_with_no_description = cls(
            prop_with_no_desc=prop_with_no_desc,
            prop_with_desc=prop_with_desc,
        )

        model_with_no_description.additional_properties = d
        return model_with_no_description

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
