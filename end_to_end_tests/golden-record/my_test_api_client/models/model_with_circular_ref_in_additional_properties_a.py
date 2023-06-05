from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.model_with_circular_ref_in_additional_properties_b import ModelWithCircularRefInAdditionalPropertiesB


T = TypeVar("T", bound="ModelWithCircularRefInAdditionalPropertiesA")


@attr.s(auto_attribs=True)
class ModelWithCircularRefInAdditionalPropertiesA:
    """ """

    additional_properties: Dict[str, "ModelWithCircularRefInAdditionalPropertiesB"] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        pass

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_with_circular_ref_in_additional_properties_b import (
            ModelWithCircularRefInAdditionalPropertiesB,
        )

        d = src_dict.copy()
        model_with_circular_ref_in_additional_properties_a = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = ModelWithCircularRefInAdditionalPropertiesB.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        model_with_circular_ref_in_additional_properties_a.additional_properties = additional_properties
        return model_with_circular_ref_in_additional_properties_a

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "ModelWithCircularRefInAdditionalPropertiesB":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "ModelWithCircularRefInAdditionalPropertiesB") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
