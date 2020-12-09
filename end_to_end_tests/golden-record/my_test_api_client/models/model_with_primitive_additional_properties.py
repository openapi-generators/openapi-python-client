from typing import Any, Dict, List, Union, cast

import attr

from ..models.model_with_primitive_additional_properties_a_date_holder import (
    ModelWithPrimitiveAdditionalPropertiesADateHolder,
)
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class ModelWithPrimitiveAdditionalProperties:
    """  """

    a_date_holder: Union[ModelWithPrimitiveAdditionalPropertiesADateHolder, Unset] = UNSET
    additional_properties: Dict[str, str] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        a_date_holder: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.a_date_holder, Unset):
            a_date_holder = self.a_date_holder.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if a_date_holder is not UNSET:
            field_dict["a_date_holder"] = a_date_holder

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "ModelWithPrimitiveAdditionalProperties":
        d = src_dict.copy()
        a_date_holder: Union[ModelWithPrimitiveAdditionalPropertiesADateHolder, Unset] = UNSET
        _a_date_holder = d.pop("a_date_holder", UNSET)
        if _a_date_holder is not None and not isinstance(_a_date_holder, Unset):
            a_date_holder = ModelWithPrimitiveAdditionalPropertiesADateHolder.from_dict(
                cast(Dict[str, Any], _a_date_holder)
            )

        model_with_primitive_additional_properties = ModelWithPrimitiveAdditionalProperties(
            a_date_holder=a_date_holder,
        )

        model_with_primitive_additional_properties.additional_properties = d
        return model_with_primitive_additional_properties

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> str:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: str) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
