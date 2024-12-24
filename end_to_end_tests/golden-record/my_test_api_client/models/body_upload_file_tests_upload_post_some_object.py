from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="BodyUploadFileTestsUploadPostSomeObject")


@_attrs_define
class BodyUploadFileTestsUploadPostSomeObject:
    """
    Attributes:
        num (float):
        text (str):
    """

    num: float
    text: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        num = self.num

        text = self.text

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "num": num,
                "text": text,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        num = d.pop("num")

        text = d.pop("text")

        body_upload_file_tests_upload_post_some_object = cls(
            num=num,
            text=text,
        )

        body_upload_file_tests_upload_post_some_object.additional_properties = d
        return body_upload_file_tests_upload_post_some_object

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
