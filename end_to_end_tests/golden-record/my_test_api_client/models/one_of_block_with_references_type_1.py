from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OneOfBlockWithReferencesType1")


@_attrs_define
class OneOfBlockWithReferencesType1:
    """
    Attributes:
        one_of_block_two (int): OneOfBlockTwoDescription
    """

    one_of_block_two: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        one_of_block_two = self.one_of_block_two

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "OneOfBlockTwo": one_of_block_two,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        one_of_block_two = d.pop("OneOfBlockTwo")

        one_of_block_with_references_type_1 = cls(
            one_of_block_two=one_of_block_two,
        )

        one_of_block_with_references_type_1.additional_properties = d
        return one_of_block_with_references_type_1

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
