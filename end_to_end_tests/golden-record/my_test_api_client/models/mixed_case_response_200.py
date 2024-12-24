from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MixedCaseResponse200")


@_attrs_define
class MixedCaseResponse200:
    """
    Attributes:
        mixed_case (Union[Unset, str]):
        mixedCase (Union[Unset, str]):
    """

    mixed_case: Union[Unset, str] = UNSET
    mixedCase: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        mixed_case = self.mixed_case

        mixedCase = self.mixedCase

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if mixed_case is not UNSET:
            field_dict["mixed_case"] = mixed_case
        if mixedCase is not UNSET:
            field_dict["mixedCase"] = mixedCase

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        mixed_case = d.pop("mixed_case", UNSET)

        mixedCase = d.pop("mixedCase", UNSET)

        mixed_case_response_200 = cls(
            mixed_case=mixed_case,
            mixedCase=mixedCase,
        )

        mixed_case_response_200.additional_properties = d
        return mixed_case_response_200

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
