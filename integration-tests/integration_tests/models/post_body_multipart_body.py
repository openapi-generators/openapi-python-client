from io import BytesIO
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, File, Unset

T = TypeVar("T", bound="PostBodyMultipartBody")


@_attrs_define
class PostBodyMultipartBody:
    """
    Attributes:
        a_string (str):
        file (File): For the sake of this test, include a file name and content type. The payload should also be valid
            UTF-8.
        description (Union[Unset, str]):
    """

    a_string: str
    file: File
    description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        a_string = self.a_string

        file = self.file.to_tuple()

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "a_string": a_string,
                "file": file,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        a_string = (None, str(self.a_string).encode(), "text/plain")

        file = self.file.to_tuple()

        description = (
            self.description
            if isinstance(self.description, Unset)
            else (None, str(self.description).encode(), "text/plain")
        )

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "a_string": a_string,
                "file": file,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        a_string = d.pop("a_string")

        file = File(payload=BytesIO(d.pop("file")))

        description = d.pop("description", UNSET)

        post_body_multipart_body = cls(
            a_string=a_string,
            file=file,
            description=description,
        )

        post_body_multipart_body.additional_properties = d
        return post_body_multipart_body

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
