from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

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
        errors (Union[Unset, List[str]]):
        extra_parameters (Union[Unset, List[str]]):
        invalid_parameters (Union[Unset, List['Problem']]):
        missing_parameters (Union[Unset, List[str]]):
    """

    errors: Union[Unset, List[str]] = UNSET
    extra_parameters: Union[Unset, List[str]] = UNSET
    invalid_parameters: Union[Unset, List["Problem"]] = UNSET
    missing_parameters: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        prop1: Union[Unset, List[str]] = UNSET
        if not isinstance(self.errors, Unset):
            prop1 = self.errors

        prop2: Union[Unset, List[str]] = UNSET
        if not isinstance(self.extra_parameters, Unset):
            prop2 = self.extra_parameters

        prop3: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.invalid_parameters, Unset):
            prop3 = []
            for invalid_parameters_item_data in self.invalid_parameters:
                invalid_parameters_item = invalid_parameters_item_data.to_dict()
                prop3.append(invalid_parameters_item)

        prop4: Union[Unset, List[str]] = UNSET
        if not isinstance(self.missing_parameters, Unset):
            prop4 = self.missing_parameters

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict = {
            **field_dict,
            **({} if prop1 is UNSET else {"errors": prop1}),
            **({} if prop2 is UNSET else {"extra_parameters": prop2}),
            **({} if prop3 is UNSET else {"invalid_parameters": prop3}),
            **({} if prop4 is UNSET else {"missing_parameters": prop4}),
        }

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.problem import Problem

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
