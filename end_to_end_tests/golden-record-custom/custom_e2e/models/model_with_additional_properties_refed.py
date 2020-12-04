from typing import Any, Dict, List

import attr

from ..models.an_enum import AnEnum


@attr.s(auto_attribs=True)
class ModelWithAdditionalPropertiesRefed:
    """  """

    additional_properties: Dict[str, AnEnum] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.value

        field_dict.update({})

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "ModelWithAdditionalPropertiesRefed":
        d = src_dict.copy()
        model_with_additional_properties_refed = ModelWithAdditionalPropertiesRefed()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = AnEnum(prop_dict)

            additional_properties[prop_name] = additional_property

        model_with_additional_properties_refed.additional_properties = additional_properties
        return model_with_additional_properties_refed

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> AnEnum:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: AnEnum) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
