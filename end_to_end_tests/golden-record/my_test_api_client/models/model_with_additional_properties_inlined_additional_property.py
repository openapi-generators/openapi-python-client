from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelWithAdditionalPropertiesInlinedAdditionalProperty")


@_attrs_define
class ModelWithAdditionalPropertiesInlinedAdditionalProperty:
    """
    Attributes:
        extra_props_prop (Union[Unset, str]):
    """

    extra_props_prop: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        prop1 = self.extra_props_prop

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict = {
            **field_dict,
            **({} if prop1 is UNSET else {"extra_props_prop": prop1}),
        }

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        extra_props_prop = d.pop("extra_props_prop", UNSET)

        model_with_additional_properties_inlined_additional_property = cls(
            extra_props_prop=extra_props_prop,
        )

        model_with_additional_properties_inlined_additional_property.additional_properties = d
        return model_with_additional_properties_inlined_additional_property

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
