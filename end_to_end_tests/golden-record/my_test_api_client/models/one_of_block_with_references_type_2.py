from typing import Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OneOfBlockWithReferencesType2")


@_attrs_define
class OneOfBlockWithReferencesType2:
    """
    Attributes:
        one_of_block_three (List[float]): OneOfBlockThreeRefDescription
    """

    one_of_block_three: List[float]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        one_of_block_three = self.one_of_block_three

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "OneOfBlockThree": one_of_block_three,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        one_of_block_three = cast(List[float], d.pop("OneOfBlockThree"))

        one_of_block_with_references_type_2 = cls(
            one_of_block_three=one_of_block_three,
        )

        one_of_block_with_references_type_2.additional_properties = d
        return one_of_block_with_references_type_2

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
