from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.an_enum import AnEnum

T = TypeVar("T", bound="ModelWithAdditionalPropertiesRefed")


@_attrs_define
class ModelWithAdditionalPropertiesRefed:
    """ """

    additional_properties: dict[str, AnEnum] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        model_with_additional_properties_refed = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = AnEnum(prop_dict)

            additional_properties[prop_name] = additional_property

        model_with_additional_properties_refed.additional_properties = additional_properties
        return model_with_additional_properties_refed

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> AnEnum:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: AnEnum) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
