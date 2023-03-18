from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.an_array_with_a_circular_ref_in_items_object_additional_properties_b_item import (
        AnArrayWithACircularRefInItemsObjectAdditionalPropertiesBItem,
    )


T = TypeVar("T", bound="AnArrayWithACircularRefInItemsObjectAdditionalPropertiesAItem")


@attr.s(auto_attribs=True)
class AnArrayWithACircularRefInItemsObjectAdditionalPropertiesAItem:
    """ """

    additional_properties: Dict[str, List["AnArrayWithACircularRefInItemsObjectAdditionalPropertiesBItem"]] = attr.ib(
        init=False, factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:
        pass

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = []
            for (
                componentsschemas_an_array_with_a_circular_ref_in_items_object_additional_properties_b_item_data
            ) in prop:
                componentsschemas_an_array_with_a_circular_ref_in_items_object_additional_properties_b_item = (
                    componentsschemas_an_array_with_a_circular_ref_in_items_object_additional_properties_b_item_data.to_dict()
                )

                field_dict[prop_name].append(
                    componentsschemas_an_array_with_a_circular_ref_in_items_object_additional_properties_b_item
                )

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.an_array_with_a_circular_ref_in_items_object_additional_properties_b_item import (
            AnArrayWithACircularRefInItemsObjectAdditionalPropertiesBItem,
        )

        d = src_dict.copy()
        an_array_with_a_circular_ref_in_items_object_additional_properties_a_item = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = []
            _additional_property = prop_dict
            for (
                componentsschemas_an_array_with_a_circular_ref_in_items_object_additional_properties_b_item_data
            ) in _additional_property:
                componentsschemas_an_array_with_a_circular_ref_in_items_object_additional_properties_b_item = (
                    AnArrayWithACircularRefInItemsObjectAdditionalPropertiesBItem.from_dict(
                        componentsschemas_an_array_with_a_circular_ref_in_items_object_additional_properties_b_item_data
                    )
                )

                additional_property.append(
                    componentsschemas_an_array_with_a_circular_ref_in_items_object_additional_properties_b_item
                )

            additional_properties[prop_name] = additional_property

        an_array_with_a_circular_ref_in_items_object_additional_properties_a_item.additional_properties = (
            additional_properties
        )
        return an_array_with_a_circular_ref_in_items_object_additional_properties_a_item

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> List["AnArrayWithACircularRefInItemsObjectAdditionalPropertiesBItem"]:
        return self.additional_properties[key]

    def __setitem__(
        self, key: str, value: List["AnArrayWithACircularRefInItemsObjectAdditionalPropertiesBItem"]
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
