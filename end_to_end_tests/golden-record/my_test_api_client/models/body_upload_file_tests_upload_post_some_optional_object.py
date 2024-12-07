from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="BodyUploadFileTestsUploadPostSomeOptionalObject")


@_attrs_define
class BodyUploadFileTestsUploadPostSomeOptionalObject:
    """
    Attributes:
        foo (str):
    """

    foo: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        foo = self.foo

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "foo": foo,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        foo = d.pop("foo")

        body_upload_file_tests_upload_post_some_optional_object = cls(
            foo=foo,
        )

        body_upload_file_tests_upload_post_some_optional_object.additional_properties = d
        return body_upload_file_tests_upload_post_some_optional_object

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
