from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="AnotherAllOfSubModel")


@attr.s(auto_attribs=True)
class AnotherAllOfSubModel:
    """  """

    another_sub_property: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        another_sub_property = self.another_sub_property

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if another_sub_property is not UNSET:
            field_dict["another_sub_property"] = another_sub_property

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        another_sub_property = d.pop("another_sub_property", UNSET)

        another_all_of_sub_model = cls(
            another_sub_property=another_sub_property,
        )

        another_all_of_sub_model.additional_properties = d
        return another_all_of_sub_model

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
