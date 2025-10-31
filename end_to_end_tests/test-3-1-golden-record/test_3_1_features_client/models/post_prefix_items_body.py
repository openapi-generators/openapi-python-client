from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostPrefixItemsBody")


@_attrs_define
class PostPrefixItemsBody:
    """
    Attributes:
        prefix_items_and_items (list[float | Literal['prefix'] | str] | Unset):
        prefix_items_only (list[float | str] | Unset):
    """

    prefix_items_and_items: list[float | Literal["prefix"] | str] | Unset = UNSET
    prefix_items_only: list[float | str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        prefix_items_and_items: list[float | Literal["prefix"] | str] | Unset = UNSET
        if not isinstance(self.prefix_items_and_items, Unset):
            prefix_items_and_items = []
            for prefix_items_and_items_item_data in self.prefix_items_and_items:
                prefix_items_and_items_item: float | Literal["prefix"] | str
                prefix_items_and_items_item = prefix_items_and_items_item_data
                prefix_items_and_items.append(prefix_items_and_items_item)

        prefix_items_only: list[float | str] | Unset = UNSET
        if not isinstance(self.prefix_items_only, Unset):
            prefix_items_only = []
            for prefix_items_only_item_data in self.prefix_items_only:
                prefix_items_only_item: float | str
                prefix_items_only_item = prefix_items_only_item_data
                prefix_items_only.append(prefix_items_only_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if prefix_items_and_items is not UNSET:
            field_dict["prefixItemsAndItems"] = prefix_items_and_items
        if prefix_items_only is not UNSET:
            field_dict["prefixItemsOnly"] = prefix_items_only

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _prefix_items_and_items = d.pop("prefixItemsAndItems", UNSET)
        prefix_items_and_items: list[float | Literal["prefix"] | str] | Unset = UNSET
        if _prefix_items_and_items is not UNSET:
            prefix_items_and_items = []
            for prefix_items_and_items_item_data in _prefix_items_and_items:

                def _parse_prefix_items_and_items_item(data: object) -> float | Literal["prefix"] | str:
                    prefix_items_and_items_item_type_0 = cast(Literal["prefix"], data)
                    if prefix_items_and_items_item_type_0 != "prefix":
                        raise ValueError(
                            f"prefixItemsAndItems_item_type_0 must match const 'prefix', got '{prefix_items_and_items_item_type_0}'"
                        )
                    return prefix_items_and_items_item_type_0
                    return cast(float | Literal["prefix"] | str, data)

                prefix_items_and_items_item = _parse_prefix_items_and_items_item(prefix_items_and_items_item_data)

                prefix_items_and_items.append(prefix_items_and_items_item)

        _prefix_items_only = d.pop("prefixItemsOnly", UNSET)
        prefix_items_only: list[float | str] | Unset = UNSET
        if _prefix_items_only is not UNSET:
            prefix_items_only = []
            for prefix_items_only_item_data in _prefix_items_only:

                def _parse_prefix_items_only_item(data: object) -> float | str:
                    return cast(float | str, data)

                prefix_items_only_item = _parse_prefix_items_only_item(prefix_items_only_item_data)

                prefix_items_only.append(prefix_items_only_item)

        post_prefix_items_body = cls(
            prefix_items_and_items=prefix_items_and_items,
            prefix_items_only=prefix_items_only,
        )

        post_prefix_items_body.additional_properties = d
        return post_prefix_items_body

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
