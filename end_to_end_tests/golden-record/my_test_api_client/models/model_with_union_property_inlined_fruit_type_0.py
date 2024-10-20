from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelWithUnionPropertyInlinedFruitType0")


@_attrs_define
class ModelWithUnionPropertyInlinedFruitType0:
    """
    Attributes:
        apples (Union[Unset, str]):
    """

    apples: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        apples = self.apples

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if apples is not UNSET:
            field_dict["apples"] = apples

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        apples = d.pop("apples", UNSET)

        model_with_union_property_inlined_fruit_type_0 = cls(
            apples=apples,
        )

        model_with_union_property_inlined_fruit_type_0.additional_properties = d
        return model_with_union_property_inlined_fruit_type_0

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
