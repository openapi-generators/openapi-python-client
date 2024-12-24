from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AnArrayWithARecursiveRefInItemsObjectItem")


@_attrs_define
class AnArrayWithARecursiveRefInItemsObjectItem:
    """
    Attributes:
        recursive (Union[Unset, list['AnArrayWithARecursiveRefInItemsObjectItem']]):
    """

    recursive: Union[Unset, list["AnArrayWithARecursiveRefInItemsObjectItem"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        recursive: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.recursive, Unset):
            recursive = []
            for componentsschemas_an_array_with_a_recursive_ref_in_items_object_item_data in self.recursive:
                componentsschemas_an_array_with_a_recursive_ref_in_items_object_item = (
                    componentsschemas_an_array_with_a_recursive_ref_in_items_object_item_data.to_dict()
                )
                recursive.append(componentsschemas_an_array_with_a_recursive_ref_in_items_object_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if recursive is not UNSET:
            field_dict["recursive"] = recursive

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        recursive = []
        _recursive = d.pop("recursive", UNSET)
        for componentsschemas_an_array_with_a_recursive_ref_in_items_object_item_data in _recursive or []:
            componentsschemas_an_array_with_a_recursive_ref_in_items_object_item = (
                AnArrayWithARecursiveRefInItemsObjectItem.from_dict(
                    componentsschemas_an_array_with_a_recursive_ref_in_items_object_item_data
                )
            )

            recursive.append(componentsschemas_an_array_with_a_recursive_ref_in_items_object_item)

        an_array_with_a_recursive_ref_in_items_object_item = cls(
            recursive=recursive,
        )

        an_array_with_a_recursive_ref_in_items_object_item.additional_properties = d
        return an_array_with_a_recursive_ref_in_items_object_item

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
