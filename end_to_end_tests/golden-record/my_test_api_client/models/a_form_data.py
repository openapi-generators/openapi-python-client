from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AFormData")


@_attrs_define
class AFormData:
    """
    Attributes:
        an_required_field (str):
        an_optional_field (Union[Unset, str]):
    """

    an_required_field: str
    an_optional_field: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        an_required_field = self.an_required_field

        an_optional_field = self.an_optional_field

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "an_required_field": an_required_field,
            }
        )
        if an_optional_field is not UNSET:
            field_dict["an_optional_field"] = an_optional_field

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        an_required_field = d.pop("an_required_field")

        an_optional_field = d.pop("an_optional_field", UNSET)

        a_form_data = cls(
            an_required_field=an_required_field,
            an_optional_field=an_optional_field,
        )

        a_form_data.additional_properties = d
        return a_form_data

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
