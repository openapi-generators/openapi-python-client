import datetime
from typing import Any, Dict, List

import attr
from dateutil.parser import isoparse


@attr.s(auto_attribs=True)
class ModelWithPrimitiveAdditionalPropertiesADateHolder:
    """  """

    additional_properties: Dict[str, datetime.datetime] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.isoformat()

        field_dict.update({})

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "ModelWithPrimitiveAdditionalPropertiesADateHolder":
        d = src_dict.copy()
        model_with_primitive_additional_properties_a_date_holder = ModelWithPrimitiveAdditionalPropertiesADateHolder()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = isoparse(prop_dict)

            additional_properties[prop_name] = additional_property

        model_with_primitive_additional_properties_a_date_holder.additional_properties = additional_properties
        return model_with_primitive_additional_properties_a_date_holder

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> datetime.datetime:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: datetime.datetime) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
