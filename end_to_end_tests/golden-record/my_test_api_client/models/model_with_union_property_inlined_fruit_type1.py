from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelWithUnionPropertyInlinedFruitType1")


@attr.s(auto_attribs=True)
class ModelWithUnionPropertyInlinedFruitType1:
    """  """

    bananas: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        bananas = self.bananas

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if bananas is not UNSET:
            field_dict["bananas"] = bananas

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        bananas = d.pop("bananas", UNSET)

        model_with_union_property_inlined_fruit_type1 = cls(
            bananas=bananas,
        )

        model_with_union_property_inlined_fruit_type1.additional_properties = d
        return model_with_union_property_inlined_fruit_type1

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
