from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelWithDescription")


@_attrs_define
class ModelWithDescription:
    """This is a nice model."""

    prop_with_no_desc: Union[Unset, str] = UNSET
    prop_with_desc: Union[Unset, str] = UNSET
    """ This is a nice property. """
    prop_with_long_desc: Union[Unset, str] = UNSET
    """ It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of
    foolishness,
    it was the epoch of belief, it was the epoch of incredulity, it was the season of light, it was the season of
    darkness, it was the spring of hope, it was the winter of despair.
     """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        prop_with_no_desc = self.prop_with_no_desc

        prop_with_desc = self.prop_with_desc

        prop_with_long_desc = self.prop_with_long_desc

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if prop_with_no_desc is not UNSET:
            field_dict["propWithNoDesc"] = prop_with_no_desc
        if prop_with_desc is not UNSET:
            field_dict["propWithDesc"] = prop_with_desc
        if prop_with_long_desc is not UNSET:
            field_dict["propWithLongDesc"] = prop_with_long_desc

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        prop_with_no_desc = d.pop("propWithNoDesc", UNSET)

        prop_with_desc = d.pop("propWithDesc", UNSET)

        prop_with_long_desc = d.pop("propWithLongDesc", UNSET)

        model_with_description = cls(
            prop_with_no_desc=prop_with_no_desc,
            prop_with_desc=prop_with_desc,
            prop_with_long_desc=prop_with_long_desc,
        )

        model_with_description.additional_properties = d
        return model_with_description

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
