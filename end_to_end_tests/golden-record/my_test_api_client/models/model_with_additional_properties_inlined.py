from typing import Any, Dict, List, Union

import attr

from ..models.model_with_additional_properties_inlined_additional_properties import (
    ModelWithAdditionalPropertiesInlinedAdditionalProperties,
)
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class ModelWithAdditionalPropertiesInlined:
    """  """

    a_number: Union[Unset, float] = UNSET
    additional_properties: Dict[str, ModelWithAdditionalPropertiesInlinedAdditionalProperties] = attr.ib(
        init=False, factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:
        a_number = self.a_number

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if a_number is not UNSET:
            field_dict["a_number"] = a_number

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "ModelWithAdditionalPropertiesInlined":
        d = src_dict.copy()
        a_number = d.pop("a_number", UNSET)

        model_with_additional_properties_inlined = ModelWithAdditionalPropertiesInlined(
            a_number=a_number,
        )

        model_with_additional_properties_inlined.additional_properties = d
        return model_with_additional_properties_inlined

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> ModelWithAdditionalPropertiesInlinedAdditionalProperties:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: ModelWithAdditionalPropertiesInlinedAdditionalProperties) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
