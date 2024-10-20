from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.an_array_with_a_circular_ref_in_items_object_a_item import AnArrayWithACircularRefInItemsObjectAItem


T = TypeVar("T", bound="AnArrayWithACircularRefInItemsObjectBItem")


@_attrs_define
class AnArrayWithACircularRefInItemsObjectBItem:
    """
    Attributes:
        circular (Union[Unset, list['AnArrayWithACircularRefInItemsObjectAItem']]):
    """

    circular: Union[Unset, list["AnArrayWithACircularRefInItemsObjectAItem"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        circular: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.circular, Unset):
            circular = []
            for componentsschemas_an_array_with_a_circular_ref_in_items_object_a_item_data in self.circular:
                componentsschemas_an_array_with_a_circular_ref_in_items_object_a_item = (
                    componentsschemas_an_array_with_a_circular_ref_in_items_object_a_item_data.to_dict()
                )
                circular.append(componentsschemas_an_array_with_a_circular_ref_in_items_object_a_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if circular is not UNSET:
            field_dict["circular"] = circular

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.an_array_with_a_circular_ref_in_items_object_a_item import (
            AnArrayWithACircularRefInItemsObjectAItem,
        )

        d = src_dict.copy()
        circular = []
        _circular = d.pop("circular", UNSET)
        for componentsschemas_an_array_with_a_circular_ref_in_items_object_a_item_data in _circular or []:
            componentsschemas_an_array_with_a_circular_ref_in_items_object_a_item = (
                AnArrayWithACircularRefInItemsObjectAItem.from_dict(
                    componentsschemas_an_array_with_a_circular_ref_in_items_object_a_item_data
                )
            )

            circular.append(componentsschemas_an_array_with_a_circular_ref_in_items_object_a_item)

        an_array_with_a_circular_ref_in_items_object_b_item = cls(
            circular=circular,
        )

        an_array_with_a_circular_ref_in_items_object_b_item.additional_properties = d
        return an_array_with_a_circular_ref_in_items_object_b_item

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
