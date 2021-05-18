from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="AModelWithDirectSelfReferenceProperty")


@attr.s(auto_attribs=True)
class AModelWithDirectSelfReferenceProperty:
    """ """

    required_self_ref: AModelWithDirectSelfReferenceProperty
    optional_self_ref: Union[Unset, AModelWithDirectSelfReferenceProperty] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        required_self_ref = self.required_self_ref
        optional_self_ref = self.optional_self_ref

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "required_self_ref": required_self_ref,
            }
        )
        if optional_self_ref is not UNSET:
            field_dict["optional_self_ref"] = optional_self_ref

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        required_self_ref = d.pop("required_self_ref")

        optional_self_ref = d.pop("optional_self_ref", UNSET)

        a_model_with_direct_self_reference_property = cls(
            required_self_ref=required_self_ref,
            optional_self_ref=optional_self_ref,
        )

        a_model_with_direct_self_reference_property.additional_properties = d
        return a_model_with_direct_self_reference_property

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
