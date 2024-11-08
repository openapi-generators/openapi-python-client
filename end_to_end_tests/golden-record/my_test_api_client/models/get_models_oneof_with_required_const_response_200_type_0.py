from typing import Any, Dict, List, Literal, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetModelsOneofWithRequiredConstResponse200Type0")


@_attrs_define
class GetModelsOneofWithRequiredConstResponse200Type0:
    """
    Attributes:
        type (Literal['alpha']):
        color (Union[Unset, str]):
    """

    type: Literal["alpha"]
    color: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        prop1 = self.type
        prop2 = self.color

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict = {
            **field_dict,
            "type": prop1,
            **({} if prop2 is UNSET else {"color": prop2}),
        }

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = cast(Literal["alpha"], d.pop("type"))
        if type != "alpha":
            raise ValueError(f"type must match const 'alpha', got '{type}'")

        color = d.pop("color", UNSET)

        get_models_oneof_with_required_const_response_200_type_0 = cls(
            type=type,
            color=color,
        )

        get_models_oneof_with_required_const_response_200_type_0.additional_properties = d
        return get_models_oneof_with_required_const_response_200_type_0

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
