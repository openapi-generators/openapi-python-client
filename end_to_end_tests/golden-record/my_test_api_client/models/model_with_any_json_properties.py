from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.model_with_any_json_properties_additional_property import ModelWithAnyJsonPropertiesAdditionalProperty


T = TypeVar("T", bound="ModelWithAnyJsonProperties")


@_attrs_define
class ModelWithAnyJsonProperties:
    """ """

    additional_properties: dict[
        str, Union["ModelWithAnyJsonPropertiesAdditionalProperty", bool, float, int, list[str], str]
    ] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.model_with_any_json_properties_additional_property import (
            ModelWithAnyJsonPropertiesAdditionalProperty,
        )

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, ModelWithAnyJsonPropertiesAdditionalProperty):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, list):
                field_dict[prop_name] = prop

            else:
                field_dict[prop_name] = prop

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.model_with_any_json_properties_additional_property import (
            ModelWithAnyJsonPropertiesAdditionalProperty,
        )

        d = src_dict.copy()
        model_with_any_json_properties = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(
                data: object,
            ) -> Union["ModelWithAnyJsonPropertiesAdditionalProperty", bool, float, int, list[str], str]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property = ModelWithAnyJsonPropertiesAdditionalProperty.from_dict(data)

                    return additional_property
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, list):
                        raise TypeError()
                    additional_property_type_1 = cast(list[str], data)

                    return additional_property_type_1
                except:  # noqa: E722
                    pass
                return cast(
                    Union["ModelWithAnyJsonPropertiesAdditionalProperty", bool, float, int, list[str], str], data
                )

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        model_with_any_json_properties.additional_properties = additional_properties
        return model_with_any_json_properties

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(
        self, key: str
    ) -> Union["ModelWithAnyJsonPropertiesAdditionalProperty", bool, float, int, list[str], str]:
        return self.additional_properties[key]

    def __setitem__(
        self, key: str, value: Union["ModelWithAnyJsonPropertiesAdditionalProperty", bool, float, int, list[str], str]
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
