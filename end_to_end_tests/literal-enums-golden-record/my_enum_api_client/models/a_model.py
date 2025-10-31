from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.an_all_of_enum import AnAllOfEnum, check_an_all_of_enum
from ..models.an_enum import AnEnum, check_an_enum
from ..models.different_enum import DifferentEnum, check_different_enum
from ..types import UNSET, Unset

T = TypeVar("T", bound="AModel")


@_attrs_define
class AModel:
    """A Model for testing all the ways enums can be used

    Attributes:
        an_enum_value (AnEnum): For testing Enums in all the ways they can be used
        an_allof_enum_with_overridden_default (AnAllOfEnum):  Default: 'overridden_default'.
        any_value (Any | Unset):
        an_optional_allof_enum (AnAllOfEnum | Unset):
        nested_list_of_enums (list[list[DifferentEnum]] | Unset):
    """

    an_enum_value: AnEnum
    an_allof_enum_with_overridden_default: AnAllOfEnum = "overridden_default"
    any_value: Any | Unset = UNSET
    an_optional_allof_enum: AnAllOfEnum | Unset = UNSET
    nested_list_of_enums: list[list[DifferentEnum]] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        an_enum_value: str = self.an_enum_value

        an_allof_enum_with_overridden_default: str = self.an_allof_enum_with_overridden_default

        any_value = self.any_value

        an_optional_allof_enum: str | Unset = UNSET
        if not isinstance(self.an_optional_allof_enum, Unset):
            an_optional_allof_enum = self.an_optional_allof_enum

        nested_list_of_enums: list[list[str]] | Unset = UNSET
        if not isinstance(self.nested_list_of_enums, Unset):
            nested_list_of_enums = []
            for nested_list_of_enums_item_data in self.nested_list_of_enums:
                nested_list_of_enums_item = []
                for nested_list_of_enums_item_item_data in nested_list_of_enums_item_data:
                    nested_list_of_enums_item_item: str = nested_list_of_enums_item_item_data
                    nested_list_of_enums_item.append(nested_list_of_enums_item_item)

                nested_list_of_enums.append(nested_list_of_enums_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "an_enum_value": an_enum_value,
                "an_allof_enum_with_overridden_default": an_allof_enum_with_overridden_default,
            }
        )
        if any_value is not UNSET:
            field_dict["any_value"] = any_value
        if an_optional_allof_enum is not UNSET:
            field_dict["an_optional_allof_enum"] = an_optional_allof_enum
        if nested_list_of_enums is not UNSET:
            field_dict["nested_list_of_enums"] = nested_list_of_enums

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        an_enum_value = check_an_enum(d.pop("an_enum_value"))

        an_allof_enum_with_overridden_default = check_an_all_of_enum(d.pop("an_allof_enum_with_overridden_default"))

        any_value = d.pop("any_value", UNSET)

        _an_optional_allof_enum = d.pop("an_optional_allof_enum", UNSET)
        an_optional_allof_enum: AnAllOfEnum | Unset
        if isinstance(_an_optional_allof_enum, Unset):
            an_optional_allof_enum = UNSET
        else:
            an_optional_allof_enum = check_an_all_of_enum(_an_optional_allof_enum)

        _nested_list_of_enums = d.pop("nested_list_of_enums", UNSET)
        nested_list_of_enums: list[list[DifferentEnum]] | Unset = UNSET
        if _nested_list_of_enums is not UNSET:
            nested_list_of_enums = []
            for nested_list_of_enums_item_data in _nested_list_of_enums:
                nested_list_of_enums_item = []
                _nested_list_of_enums_item = nested_list_of_enums_item_data
                for nested_list_of_enums_item_item_data in _nested_list_of_enums_item:
                    nested_list_of_enums_item_item = check_different_enum(nested_list_of_enums_item_item_data)

                    nested_list_of_enums_item.append(nested_list_of_enums_item_item)

                nested_list_of_enums.append(nested_list_of_enums_item)

        a_model = cls(
            an_enum_value=an_enum_value,
            an_allof_enum_with_overridden_default=an_allof_enum_with_overridden_default,
            any_value=any_value,
            an_optional_allof_enum=an_optional_allof_enum,
            nested_list_of_enums=nested_list_of_enums,
        )

        return a_model
