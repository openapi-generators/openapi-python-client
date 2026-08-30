from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.property_escapes_model_title_printuh_oh_escaped_enum import PropertyEscapesModelTitlePrintuhOhEscapedEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="PropertyEscapesModelTitlePrintuhOh")


@_attrs_define
class PropertyEscapesModelTitlePrintuhOh:
    """
    Attributes:
        escaped_description (str | Unset): Attempting to escape the Attributes docstring \"\"\" print('uh oh') Default:
            'default value with \\\\"quotes\\\\"'. Example: Example \"\"\" print('uh oh').
        escaped_enum (PropertyEscapesModelTitlePrintuhOhEscapedEnum | Unset):
        escaped_const (Literal['\\\\" + print(\\'uh oh\\') + \\\\"'] | Unset):
    """

    escaped_description: str | Unset = 'default value with \\"quotes\\"'
    escaped_enum: PropertyEscapesModelTitlePrintuhOhEscapedEnum | Unset = UNSET
    escaped_const: Literal["\\\" + print('uh oh') + \\\""] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        escaped_description = self.escaped_description

        escaped_enum: str | Unset = UNSET
        if not isinstance(self.escaped_enum, Unset):
            escaped_enum = self.escaped_enum.value

        escaped_const = self.escaped_const

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if escaped_description is not UNSET:
            field_dict["escaped_description"] = escaped_description
        if escaped_enum is not UNSET:
            field_dict["escaped_enum"] = escaped_enum
        if escaped_const is not UNSET:
            field_dict["escaped_const"] = escaped_const

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        escaped_description = d.pop("escaped_description", UNSET)

        _escaped_enum = d.pop("escaped_enum", UNSET)
        escaped_enum: PropertyEscapesModelTitlePrintuhOhEscapedEnum | Unset
        if isinstance(_escaped_enum, Unset):
            escaped_enum = UNSET
        else:
            escaped_enum = PropertyEscapesModelTitlePrintuhOhEscapedEnum(_escaped_enum)

        escaped_const = cast(Literal["\\\" + print('uh oh') + \\\""] | Unset, d.pop("escaped_const", UNSET))
        if escaped_const != "\\\" + print('uh oh') + \\\"" and not isinstance(escaped_const, Unset):
            raise ValueError(
                f"escaped_const must match const '\\\\\" + print(\\'uh oh\\') + \\\\\"', got '{escaped_const}'"
            )

        property_escapes_model_title_printuh_oh = cls(
            escaped_description=escaped_description,
            escaped_enum=escaped_enum,
            escaped_const=escaped_const,
        )

        property_escapes_model_title_printuh_oh.additional_properties = d
        return property_escapes_model_title_printuh_oh

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
