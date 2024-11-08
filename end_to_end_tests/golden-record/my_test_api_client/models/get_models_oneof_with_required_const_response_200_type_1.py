from typing import Any, Dict, List, Literal, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetModelsOneofWithRequiredConstResponse200Type1")


@_attrs_define
class GetModelsOneofWithRequiredConstResponse200Type1:
    """
    Attributes:
        type (Literal['beta']):
        texture (Union[Unset, str]):
    """

    type: Literal["beta"]
    texture: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        prop1 = self.type
        prop2 = self.texture

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict = {
            **field_dict,
            "type": prop1,
            **({} if prop2 is UNSET else {"texture": prop2}),
        }

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = cast(Literal["beta"], d.pop("type"))
        if type != "beta":
            raise ValueError(f"type must match const 'beta', got '{type}'")

        texture = d.pop("texture", UNSET)

        get_models_oneof_with_required_const_response_200_type_1 = cls(
            type=type,
            texture=texture,
        )

        get_models_oneof_with_required_const_response_200_type_1.additional_properties = d
        return get_models_oneof_with_required_const_response_200_type_1

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
