from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from .. import types
from ..models.an_all_of_enum import AnAllOfEnum, check_an_all_of_enum
from ..models.an_enum import AnEnum, check_an_enum
from ..models.an_enum_with_null import AnEnumWithNull, check_an_enum_with_null
from ..models.different_enum import DifferentEnum, check_different_enum
from ..types import UNSET, Unset

T = TypeVar("T", bound="PostUserListBody")


@_attrs_define
class PostUserListBody:
    """
    Attributes:
        an_enum_value (list[AnEnum] | Unset):
        an_enum_value_with_null (list[AnEnumWithNull | None] | Unset):
        an_enum_value_with_only_null (list[None] | Unset):
        an_allof_enum_with_overridden_default (AnAllOfEnum | Unset):  Default: 'overridden_default'.
        an_optional_allof_enum (AnAllOfEnum | Unset):
        nested_list_of_enums (list[list[DifferentEnum]] | Unset):
    """

    an_enum_value: list[AnEnum] | Unset = UNSET
    an_enum_value_with_null: list[AnEnumWithNull | None] | Unset = UNSET
    an_enum_value_with_only_null: list[None] | Unset = UNSET
    an_allof_enum_with_overridden_default: AnAllOfEnum | Unset = "overridden_default"
    an_optional_allof_enum: AnAllOfEnum | Unset = UNSET
    nested_list_of_enums: list[list[DifferentEnum]] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        an_enum_value: list[str] | Unset = UNSET
        if not isinstance(self.an_enum_value, Unset):
            an_enum_value = []
            for an_enum_value_item_data in self.an_enum_value:
                an_enum_value_item: str = an_enum_value_item_data
                an_enum_value.append(an_enum_value_item)

        an_enum_value_with_null: list[None | str] | Unset = UNSET
        if not isinstance(self.an_enum_value_with_null, Unset):
            an_enum_value_with_null = []
            for an_enum_value_with_null_item_data in self.an_enum_value_with_null:
                an_enum_value_with_null_item: None | str
                if isinstance(an_enum_value_with_null_item_data, str):
                    an_enum_value_with_null_item = an_enum_value_with_null_item_data
                else:
                    an_enum_value_with_null_item = an_enum_value_with_null_item_data
                an_enum_value_with_null.append(an_enum_value_with_null_item)

        an_enum_value_with_only_null: list[None] | Unset = UNSET
        if not isinstance(self.an_enum_value_with_only_null, Unset):
            an_enum_value_with_only_null = self.an_enum_value_with_only_null

        an_allof_enum_with_overridden_default: str | Unset = UNSET
        if not isinstance(self.an_allof_enum_with_overridden_default, Unset):
            an_allof_enum_with_overridden_default = self.an_allof_enum_with_overridden_default

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
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if an_enum_value is not UNSET:
            field_dict["an_enum_value"] = an_enum_value
        if an_enum_value_with_null is not UNSET:
            field_dict["an_enum_value_with_null"] = an_enum_value_with_null
        if an_enum_value_with_only_null is not UNSET:
            field_dict["an_enum_value_with_only_null"] = an_enum_value_with_only_null
        if an_allof_enum_with_overridden_default is not UNSET:
            field_dict["an_allof_enum_with_overridden_default"] = an_allof_enum_with_overridden_default
        if an_optional_allof_enum is not UNSET:
            field_dict["an_optional_allof_enum"] = an_optional_allof_enum
        if nested_list_of_enums is not UNSET:
            field_dict["nested_list_of_enums"] = nested_list_of_enums

        return field_dict

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        if not isinstance(self.an_enum_value, Unset):
            for an_enum_value_item_element in self.an_enum_value:
                files.append(("an_enum_value", (None, str(an_enum_value_item_element).encode(), "text/plain")))

        if not isinstance(self.an_enum_value_with_null, Unset):
            for an_enum_value_with_null_item_element in self.an_enum_value_with_null:
                if an_enum_value_with_null_item_element is None:
                    files.append(
                        (
                            "an_enum_value_with_null",
                            (None, str(an_enum_value_with_null_item_element).encode(), "text/plain"),
                        )
                    )
                else:
                    files.append(
                        (
                            "an_enum_value_with_null",
                            (None, str(an_enum_value_with_null_item_element).encode(), "text/plain"),
                        )
                    )

        if not isinstance(self.an_enum_value_with_only_null, Unset):
            for an_enum_value_with_only_null_item_element in self.an_enum_value_with_only_null:
                files.append(
                    (
                        "an_enum_value_with_only_null",
                        (None, str(an_enum_value_with_only_null_item_element).encode(), "text/plain"),
                    )
                )

        if not isinstance(self.an_allof_enum_with_overridden_default, Unset):
            files.append(
                (
                    "an_allof_enum_with_overridden_default",
                    (None, str(self.an_allof_enum_with_overridden_default).encode(), "text/plain"),
                )
            )

        if not isinstance(self.an_optional_allof_enum, Unset):
            files.append(("an_optional_allof_enum", (None, str(self.an_optional_allof_enum).encode(), "text/plain")))

        if not isinstance(self.nested_list_of_enums, Unset):
            for nested_list_of_enums_item_element in self.nested_list_of_enums:
                for nested_list_of_enums_item_item_element in nested_list_of_enums_item_element:
                    files.append(
                        (
                            "nested_list_of_enums",
                            (None, str(nested_list_of_enums_item_item_element).encode(), "text/plain"),
                        )
                    )

        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _an_enum_value = d.pop("an_enum_value", UNSET)
        an_enum_value: list[AnEnum] | Unset = UNSET
        if _an_enum_value is not UNSET:
            an_enum_value = []
            for an_enum_value_item_data in _an_enum_value:
                an_enum_value_item = check_an_enum(an_enum_value_item_data)

                an_enum_value.append(an_enum_value_item)

        _an_enum_value_with_null = d.pop("an_enum_value_with_null", UNSET)
        an_enum_value_with_null: list[AnEnumWithNull | None] | Unset = UNSET
        if _an_enum_value_with_null is not UNSET:
            an_enum_value_with_null = []
            for an_enum_value_with_null_item_data in _an_enum_value_with_null:

                def _parse_an_enum_value_with_null_item(data: object) -> AnEnumWithNull | None:
                    if data is None:
                        return data
                    try:
                        if not isinstance(data, str):
                            raise TypeError()
                        componentsschemas_an_enum_with_null_type_1 = check_an_enum_with_null(data)

                        return componentsschemas_an_enum_with_null_type_1
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    return cast(AnEnumWithNull | None, data)

                an_enum_value_with_null_item = _parse_an_enum_value_with_null_item(an_enum_value_with_null_item_data)

                an_enum_value_with_null.append(an_enum_value_with_null_item)

        an_enum_value_with_only_null = cast(list[None], d.pop("an_enum_value_with_only_null", UNSET))

        _an_allof_enum_with_overridden_default = d.pop("an_allof_enum_with_overridden_default", UNSET)
        an_allof_enum_with_overridden_default: AnAllOfEnum | Unset
        if isinstance(_an_allof_enum_with_overridden_default, Unset):
            an_allof_enum_with_overridden_default = UNSET
        else:
            an_allof_enum_with_overridden_default = check_an_all_of_enum(_an_allof_enum_with_overridden_default)

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

        post_user_list_body = cls(
            an_enum_value=an_enum_value,
            an_enum_value_with_null=an_enum_value_with_null,
            an_enum_value_with_only_null=an_enum_value_with_only_null,
            an_allof_enum_with_overridden_default=an_allof_enum_with_overridden_default,
            an_optional_allof_enum=an_optional_allof_enum,
            nested_list_of_enums=nested_list_of_enums,
        )

        post_user_list_body.additional_properties = d
        return post_user_list_body

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
