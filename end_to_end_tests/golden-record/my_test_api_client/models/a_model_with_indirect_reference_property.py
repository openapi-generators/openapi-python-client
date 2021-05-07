from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.an_enum import AnEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="AModelWithIndirectReferenceProperty")


@attr.s(auto_attribs=True)
class AModelWithIndirectReferenceProperty:
    """ """

    an_enum_indirect_ref: Union[Unset, AnEnum] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        an_enum_indirect_ref: Union[Unset, str] = UNSET
        if not isinstance(self.an_enum_indirect_ref, Unset):
            an_enum_indirect_ref = self.an_enum_indirect_ref.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if an_enum_indirect_ref is not UNSET:
            field_dict["an_enum_indirect_ref"] = an_enum_indirect_ref

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        an_enum_indirect_ref: Union[Unset, AnEnum] = UNSET
        _an_enum_indirect_ref = d.pop("an_enum_indirect_ref", UNSET)
        if not isinstance(_an_enum_indirect_ref, Unset):
            an_enum_indirect_ref = AnEnum(_an_enum_indirect_ref)

        a_model_with_indirect_reference_property = cls(
            an_enum_indirect_ref=an_enum_indirect_ref,
        )

        a_model_with_indirect_reference_property.additional_properties = d
        return a_model_with_indirect_reference_property

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
