from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetModelsOneofWithRequiredConstResponse200Type1")


@_attrs_define
class GetModelsOneofWithRequiredConstResponse200Type1:
    """
    Attributes:
        type_ (Literal['beta']):
        texture (Union[Unset, str]):
    """

    type_: Literal["beta"]
    texture: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        texture = self.texture

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
            }
        )
        if texture is not UNSET:
            field_dict["texture"] = texture

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        type_ = cast(Literal["beta"], d.pop("type"))
        if type_ != "beta":
            raise ValueError(f"type must match const 'beta', got '{type_}'")

        texture = d.pop("texture", UNSET)

        get_models_oneof_with_required_const_response_200_type_1 = cls(
            type_=type_,
            texture=texture,
        )

        get_models_oneof_with_required_const_response_200_type_1.additional_properties = d
        return get_models_oneof_with_required_const_response_200_type_1

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
