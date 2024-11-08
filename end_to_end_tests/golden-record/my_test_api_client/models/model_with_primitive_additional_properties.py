from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_with_primitive_additional_properties_a_date_holder import (
        ModelWithPrimitiveAdditionalPropertiesADateHolder,
    )


T = TypeVar("T", bound="ModelWithPrimitiveAdditionalProperties")


@_attrs_define
class ModelWithPrimitiveAdditionalProperties:
    """
    Attributes:
        a_date_holder (Union[Unset, ModelWithPrimitiveAdditionalPropertiesADateHolder]):
    """

    a_date_holder: Union[Unset, "ModelWithPrimitiveAdditionalPropertiesADateHolder"] = UNSET
    additional_properties: Dict[str, str] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        prop1: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.a_date_holder, Unset):
            prop1 = self.a_date_holder.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict = {
            **field_dict,
            **({} if prop1 is UNSET else {"a_date_holder": prop1}),
        }

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_with_primitive_additional_properties_a_date_holder import (
            ModelWithPrimitiveAdditionalPropertiesADateHolder,
        )

        d = src_dict.copy()
        _a_date_holder = d.pop("a_date_holder", UNSET)
        a_date_holder: Union[Unset, ModelWithPrimitiveAdditionalPropertiesADateHolder]
        if isinstance(_a_date_holder, Unset):
            a_date_holder = UNSET
        else:
            a_date_holder = ModelWithPrimitiveAdditionalPropertiesADateHolder.from_dict(_a_date_holder)

        model_with_primitive_additional_properties = cls(
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
