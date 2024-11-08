from typing import Any, Dict, List, Type, TypeVar, Union

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
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        prop1 = self.mixed_case
        prop2 = self.mixedCase

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict = {
            **field_dict,
            **({} if prop1 is UNSET else {"mixed_case": prop1}),
            **({} if prop2 is UNSET else {"mixedCase": prop2}),
        }

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
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
