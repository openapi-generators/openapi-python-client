from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_with_additional_properties_inlined_additional_property import (
        ModelWithAdditionalPropertiesInlinedAdditionalProperty,
    )


T = TypeVar("T", bound="ModelWithAdditionalPropertiesInlined")


@_attrs_define
class ModelWithAdditionalPropertiesInlined:
    """
    Attributes:
        a_number (Union[Unset, float]):
    """

    a_number: Union[Unset, float] = UNSET
    additional_properties: Dict[str, "ModelWithAdditionalPropertiesInlinedAdditionalProperty"] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:
        prop1 = self.a_number

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()
        field_dict = {
            **field_dict,
            **({} if prop1 is UNSET else {"a_number": prop1}),
        }

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_with_additional_properties_inlined_additional_property import (
            ModelWithAdditionalPropertiesInlinedAdditionalProperty,
        )

        d = src_dict.copy()
        a_number = d.pop("a_number", UNSET)

        model_with_additional_properties_inlined = cls(
            a_number=a_number,
        )

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = ModelWithAdditionalPropertiesInlinedAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        model_with_additional_properties_inlined.additional_properties = additional_properties
        return model_with_additional_properties_inlined

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "ModelWithAdditionalPropertiesInlinedAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "ModelWithAdditionalPropertiesInlinedAdditionalProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
