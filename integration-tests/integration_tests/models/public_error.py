from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.problem import Problem
from ..types import UNSET, Unset

T = TypeVar("T", bound="PublicError")


@attr.s(auto_attribs=True)
class PublicError:
    """
    Attributes:
        errors (Union[Unset, List[str]]):
        extra_parameters (Union[Unset, List[str]]):
        invalid_parameters (Union[Unset, List[Problem]]):
        missing_parameters (Union[Unset, List[str]]):
    """

    errors: Union[Unset, List[str]] = UNSET
    extra_parameters: Union[Unset, List[str]] = UNSET
    invalid_parameters: Union[Unset, List[Problem]] = UNSET
    missing_parameters: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        errors: Union[Unset, List[str]] = UNSET
        if not isinstance(self.errors, Unset):
            errors = self.errors

        extra_parameters: Union[Unset, List[str]] = UNSET
        if not isinstance(self.extra_parameters, Unset):
            extra_parameters = self.extra_parameters

        invalid_parameters: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.invalid_parameters, Unset):
            invalid_parameters = []
            for invalid_parameters_item_data in self.invalid_parameters:
                invalid_parameters_item = invalid_parameters_item_data.to_dict()

                invalid_parameters.append(invalid_parameters_item)

        missing_parameters: Union[Unset, List[str]] = UNSET
        if not isinstance(self.missing_parameters, Unset):
            missing_parameters = self.missing_parameters

        field_dict: Dict[str, Any] = {}
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
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        errors = cast(List[str], d.pop("errors", UNSET))

        extra_parameters = cast(List[str], d.pop("extra_parameters", UNSET))

        invalid_parameters = []
        _invalid_parameters = d.pop("invalid_parameters", UNSET)
        for invalid_parameters_item_data in _invalid_parameters or []:
            invalid_parameters_item = Problem.from_dict(invalid_parameters_item_data)

            invalid_parameters.append(invalid_parameters_item)

        missing_parameters = cast(List[str], d.pop("missing_parameters", UNSET))

        public_error = cls(
            errors=errors,
            extra_parameters=extra_parameters,
            invalid_parameters=invalid_parameters,
            missing_parameters=missing_parameters,
        )

        public_error.additional_properties = d
        return public_error

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
