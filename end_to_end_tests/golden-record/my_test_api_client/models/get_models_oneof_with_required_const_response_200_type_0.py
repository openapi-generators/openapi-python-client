from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetModelsOneofWithRequiredConstResponse200Type0")


@_attrs_define
class GetModelsOneofWithRequiredConstResponse200Type0:
    """
    Attributes:
        type_ (Literal['alpha']):
        color (Union[Unset, str]):
    """

    type_: Literal["alpha"]
    color: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        color = self.color

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
            }
        )
        if color is not UNSET:
            field_dict["color"] = color

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        type_ = cast(Literal["alpha"], d.pop("type"))
        if type_ != "alpha":
            raise ValueError(f"type must match const 'alpha', got '{type_}'")

        color = d.pop("color", UNSET)

        get_models_oneof_with_required_const_response_200_type_0 = cls(
            type_=type_,
            color=color,
        )

        get_models_oneof_with_required_const_response_200_type_0.additional_properties = d
        return get_models_oneof_with_required_const_response_200_type_0

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
