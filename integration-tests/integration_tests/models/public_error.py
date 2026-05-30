from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.problem import Problem


T = TypeVar("T", bound="PublicError")


@_attrs_define
class PublicError:
    """
    Attributes:
        errors (list[str] | Unset):
        extra_parameters (list[str] | Unset):
        invalid_parameters (list[Problem] | Unset):
        missing_parameters (list[str] | Unset):
    """

    errors: list[str] | Unset = UNSET
    extra_parameters: list[str] | Unset = UNSET
    invalid_parameters: list[Problem] | Unset = UNSET
    missing_parameters: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        errors: list[str] | Unset = UNSET
        if not isinstance(self.errors, Unset):
            errors = self.errors

        extra_parameters: list[str] | Unset = UNSET
        if not isinstance(self.extra_parameters, Unset):
            extra_parameters = self.extra_parameters

        invalid_parameters: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.invalid_parameters, Unset):
            invalid_parameters = []
            for invalid_parameters_item_data in self.invalid_parameters:
                invalid_parameters_item = invalid_parameters_item_data.to_dict()
                invalid_parameters.append(invalid_parameters_item)

        missing_parameters: list[str] | Unset = UNSET
        if not isinstance(self.missing_parameters, Unset):
            missing_parameters = self.missing_parameters

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if errors is not UNSET:
            field_dict["errors"] = errors
        if extra_parameters is not UNSET:
            field_dict["extra_parameters"] = extra_parameters
        if invalid_parameters is not UNSET:
            field_dict["invalid_parameters"] = invalid_parameters
        if missing_parameters is not UNSET:
            field_dict["missing_parameters"] = missing_parameters

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.problem import Problem

        d = dict(src_dict)
        errors = cast(list[str], d.pop("errors", UNSET))

        extra_parameters = cast(list[str], d.pop("extra_parameters", UNSET))

        _invalid_parameters = d.pop("invalid_parameters", UNSET)
        invalid_parameters: list[Problem] | Unset = UNSET
        if _invalid_parameters is not UNSET:
            invalid_parameters = []
            for invalid_parameters_item_data in _invalid_parameters:
                invalid_parameters_item = Problem.from_dict(invalid_parameters_item_data)

                invalid_parameters.append(invalid_parameters_item)

        missing_parameters = cast(list[str], d.pop("missing_parameters", UNSET))

        public_error = cls(
            errors=errors,
            extra_parameters=extra_parameters,
            invalid_parameters=invalid_parameters,
            missing_parameters=missing_parameters,
        )

        public_error.additional_properties = d
        return public_error

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
