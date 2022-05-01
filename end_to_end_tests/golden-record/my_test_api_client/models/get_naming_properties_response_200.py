from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetNamingPropertiesResponse200")


@attr.s(auto_attribs=True)
class GetNamingPropertiesResponse200:
    """
    Attributes:
        private (Union[Unset, str]):
        a (Union[Unset, str]):
        postfix (Union[Unset, str]):
    """

    private: Union[Unset, str] = UNSET
    a: Union[Unset, str] = UNSET
    postfix: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        private = self.private
        a = self.a
        postfix = self.postfix

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if private is not UNSET:
            field_dict["_a"] = private
        if a is not UNSET:
            field_dict["a"] = a
        if postfix is not UNSET:
            field_dict["a_"] = postfix

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        private = d.pop("_a", UNSET)

        a = d.pop("a", UNSET)

        postfix = d.pop("a_", UNSET)

        get_naming_properties_response_200 = cls(
            private=private,
            a=a,
            postfix=postfix,
        )

        get_naming_properties_response_200.additional_properties = d
        return get_naming_properties_response_200

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
