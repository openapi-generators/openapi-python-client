from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AllOfRequiredBase")


@_attrs_define
class AllOfRequiredBase:
    """
    Attributes:
        bar (str | Unset): The bar property
        baz (str | Unset): The baz property
    """

    bar: str | Unset = UNSET
    baz: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        bar = self.bar

        baz = self.baz

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if bar is not UNSET:
            field_dict["bar"] = bar
        if baz is not UNSET:
            field_dict["baz"] = baz

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        bar = d.pop("bar", UNSET)

        baz = d.pop("baz", UNSET)

        all_of_required_base = cls(
            bar=bar,
            baz=baz,
        )

        all_of_required_base.additional_properties = d
        return all_of_required_base

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
