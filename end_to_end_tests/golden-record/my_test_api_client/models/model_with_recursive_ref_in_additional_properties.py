from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ModelWithRecursiveRefInAdditionalProperties")


@_attrs_define
class ModelWithRecursiveRefInAdditionalProperties:
    """ """

    additional_properties: Dict[str, "ModelWithRecursiveRefInAdditionalProperties"] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        model_with_recursive_ref_in_additional_properties = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = ModelWithRecursiveRefInAdditionalProperties.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        model_with_recursive_ref_in_additional_properties.additional_properties = additional_properties
        return model_with_recursive_ref_in_additional_properties

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "ModelWithRecursiveRefInAdditionalProperties":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "ModelWithRecursiveRefInAdditionalProperties") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
