from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.model_with_any_json_properties_additional_property_type0 import (
    ModelWithAnyJsonPropertiesAdditionalPropertyType0,
)

T = TypeVar("T", bound="ModelWithAnyJsonProperties")


@attr.s(auto_attribs=True)
class ModelWithAnyJsonProperties:
    """  """

    additional_properties: Dict[
        str, Union[List[str], ModelWithAnyJsonPropertiesAdditionalPropertyType0, bool, float, int, str]
    ] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, ModelWithAnyJsonPropertiesAdditionalPropertyType0):
                field_dict[prop_name] = prop.to_dict()

            elif isinstance(prop, list):
                field_dict[prop_name] = prop

            else:
                field_dict[prop_name] = prop

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        model_with_any_json_properties = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(
                data: object,
            ) -> Union[List[str], ModelWithAnyJsonPropertiesAdditionalPropertyType0, bool, float, int, str]:
                try:
                    additional_property_type0: ModelWithAnyJsonPropertiesAdditionalPropertyType0
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type0 = ModelWithAnyJsonPropertiesAdditionalPropertyType0.from_dict(data)

                    return additional_property_type0
                except:  # noqa: E722
                    pass
                try:
                    additional_property_type1: List[str]
                    if not isinstance(data, list):
                        raise TypeError()
                    additional_property_type1 = cast(List[str], data)

                    return additional_property_type1
                except:  # noqa: E722
                    pass
                return cast(
                    Union[List[str], ModelWithAnyJsonPropertiesAdditionalPropertyType0, bool, float, int, str], data
                )

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        model_with_any_json_properties.additional_properties = additional_properties
        return model_with_any_json_properties

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(
        self, key: str
    ) -> Union[List[str], ModelWithAnyJsonPropertiesAdditionalPropertyType0, bool, float, int, str]:
        return self.additional_properties[key]

    def __setitem__(
        self,
        key: str,
        value: Union[List[str], ModelWithAnyJsonPropertiesAdditionalPropertyType0, bool, float, int, str],
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
