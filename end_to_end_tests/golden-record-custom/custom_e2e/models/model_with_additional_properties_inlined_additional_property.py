from typing import Any, Dict, List, Union

import attr

from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class ModelWithAdditionalPropertiesInlinedAdditionalProperty:
    """  """

    extra_props_prop: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        extra_props_prop = self.extra_props_prop

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if extra_props_prop is not UNSET:
            field_dict["extra_props_prop"] = extra_props_prop

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "ModelWithAdditionalPropertiesInlinedAdditionalProperty":
        d = src_dict.copy()
        extra_props_prop = d.pop("extra_props_prop", UNSET)

        model_with_additional_properties_inlined_additional_property = (
            ModelWithAdditionalPropertiesInlinedAdditionalProperty(
                extra_props_prop=extra_props_prop,
            )
        )

        model_with_additional_properties_inlined_additional_property.additional_properties = d
        return model_with_additional_properties_inlined_additional_property

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
