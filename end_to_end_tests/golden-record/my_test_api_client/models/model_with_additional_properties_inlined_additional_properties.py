from typing import Any, Dict, Union

import attr

from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class ModelWithAdditionalPropertiesInlinedAdditionalProperties:
    """  """

    extra_props_prop: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        extra_props_prop = self.extra_props_prop

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if extra_props_prop is not UNSET:
            field_dict["extra_props_prop"] = extra_props_prop

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "ModelWithAdditionalPropertiesInlinedAdditionalProperties":
        d = src_dict.copy()
        extra_props_prop = d.pop("extra_props_prop", UNSET)

        model_with_additional_properties_inlined_additional_properties = (
            ModelWithAdditionalPropertiesInlinedAdditionalProperties(
                extra_props_prop=extra_props_prop,
            )
        )

        return model_with_additional_properties_inlined_additional_properties
