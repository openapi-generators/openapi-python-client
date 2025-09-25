from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelWithUnionPropertyInlinedBananas")


@_attrs_define
class ModelWithUnionPropertyInlinedBananas:
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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        bananas = d.pop("bananas", UNSET)

        model_with_union_property_inlined_bananas = cls(
            bananas=bananas,
        )

        model_with_union_property_inlined_bananas.additional_properties = d
        return model_with_union_property_inlined_bananas

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
