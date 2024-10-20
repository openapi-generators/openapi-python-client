from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelWithUnionPropertyInlinedFruitType1")


@_attrs_define
class ModelWithUnionPropertyInlinedFruitType1:
    """
    Attributes:
        bananas (Union[Unset, str]):
    """

    bananas: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        bananas = self.bananas

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if bananas is not UNSET:
            field_dict["bananas"] = bananas

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        bananas = d.pop("bananas", UNSET)

        model_with_union_property_inlined_fruit_type_1 = cls(
            bananas=bananas,
        )

        model_with_union_property_inlined_fruit_type_1.additional_properties = d
        return model_with_union_property_inlined_fruit_type_1

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
