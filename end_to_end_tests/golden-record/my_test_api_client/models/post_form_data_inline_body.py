from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostFormDataInlineBody")


@_attrs_define
class PostFormDataInlineBody:
    """
    Attributes:
        a_required_field (str):
        an_optional_field (Union[Unset, str]):
    """

    a_required_field: str
    an_optional_field: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        a_required_field = self.a_required_field

        an_optional_field = self.an_optional_field

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "a_required_field": a_required_field,
            }
        )
        if an_optional_field is not UNSET:
            field_dict["an_optional_field"] = an_optional_field

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        a_required_field = d.pop("a_required_field")

        an_optional_field = d.pop("an_optional_field", UNSET)

        post_form_data_inline_body = cls(
            a_required_field=a_required_field,
            an_optional_field=an_optional_field,
        )

        post_form_data_inline_body.additional_properties = d
        return post_form_data_inline_body

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
