from typing import Any, Dict, List, Union, cast

import attr

from ..models.model_with_any_json_properties_additional_property import ModelWithAnyJsonPropertiesAdditionalProperty
from ..types import Unset


@attr.s(auto_attribs=True)
class ModelWithAnyJsonProperties:
    """  """

    additional_properties: Dict[
        str, Union[ModelWithAnyJsonPropertiesAdditionalProperty, List[str], str, float, int, bool]
    ] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, ModelWithAnyJsonPropertiesAdditionalProperty):
                field_dict[prop_name] = prop.to_dict()

            elif isinstance(prop, list):
                field_dict[prop_name] = prop

            else:
                field_dict[prop_name] = prop

        field_dict.update({})

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "ModelWithAnyJsonProperties":
        d = src_dict.copy()
        model_with_any_json_properties = ModelWithAnyJsonProperties()

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(
                data: Any,
            ) -> Union[ModelWithAnyJsonPropertiesAdditionalProperty, List[str], str, float, int, bool]:
                data = None if isinstance(data, Unset) else data
                additional_property: Union[
                    ModelWithAnyJsonPropertiesAdditionalProperty, List[str], str, float, int, bool
                ]
                try:
                    additional_property = ModelWithAnyJsonPropertiesAdditionalProperty.from_dict(data)

                    return additional_property
                except:  # noqa: E722
                    pass
                try:
                    additional_property = cast(List[str], data)

                    return additional_property
                except:  # noqa: E722
                    pass
                return cast(Union[ModelWithAnyJsonPropertiesAdditionalProperty, List[str], str, float, int, bool], data)

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        model_with_any_json_properties.additional_properties = additional_properties
        return model_with_any_json_properties

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(
        self, key: str
    ) -> Union[ModelWithAnyJsonPropertiesAdditionalProperty, List[str], str, float, int, bool]:
        return self.additional_properties[key]

    def __setitem__(
        self, key: str, value: Union[ModelWithAnyJsonPropertiesAdditionalProperty, List[str], str, float, int, bool]
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
