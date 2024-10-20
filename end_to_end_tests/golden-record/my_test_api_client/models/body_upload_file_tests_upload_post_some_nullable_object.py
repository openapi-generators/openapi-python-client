from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BodyUploadFileTestsUploadPostSomeNullableObject")


@_attrs_define
class BodyUploadFileTestsUploadPostSomeNullableObject:
    """
    Attributes:
        bar (Union[Unset, str]):
    """

    bar: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        bar = self.bar

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if bar is not UNSET:
            field_dict["bar"] = bar

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        bar = d.pop("bar", UNSET)

        body_upload_file_tests_upload_post_some_nullable_object = cls(
            bar=bar,
        )

        body_upload_file_tests_upload_post_some_nullable_object.additional_properties = d
        return body_upload_file_tests_upload_post_some_nullable_object

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
