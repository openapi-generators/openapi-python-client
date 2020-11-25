from typing import Any, Dict, List

import attr

from ..models.an_enum import AnEnum


@attr.s(auto_attribs=True)
class ModelWithAdditionalPropertiesRefed:
    """  """

    _additional_properties: Dict[str, AnEnum] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        field_dict.update(self._additional_properties)
        field_dict.update({})

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "ModelWithAdditionalPropertiesRefed":
        d = src_dict.copy()
        model_with_additional_properties_refed = ModelWithAdditionalPropertiesRefed()

        model_with_additional_properties_refed._additional_properties.update(d)
        return model_with_additional_properties_refed

    @property
    def additional_properties(self) -> Dict[str, AnEnum]:
        return self._additional_properties

    @property
    def additional_keys(self) -> List[str]:
        return list(self._additional_properties.keys())

    def __getitem__(self, key: str) -> AnEnum:
        return self._additional_properties[key]

    def __setitem__(self, key: str, value: AnEnum) -> None:
        self._additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self._additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self._additional_properties
