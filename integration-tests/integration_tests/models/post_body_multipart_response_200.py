from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.post_body_multipart_response_200_files_item import PostBodyMultipartResponse200FilesItem


T = TypeVar("T", bound="PostBodyMultipartResponse200")


@_attrs_define
class PostBodyMultipartResponse200:
    """
    Attributes:
        a_string (str): Echo of the 'a_string' input parameter from the form.
        description (str): Echo of the 'description' input parameter from the form.
        files (list['PostBodyMultipartResponse200FilesItem']):
    """

    a_string: str
    description: str
    files: list["PostBodyMultipartResponse200FilesItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        a_string = self.a_string

        description = self.description

        files = []
        for files_item_data in self.files:
            files_item = files_item_data.to_dict()
            files.append(files_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "a_string": a_string,
                "description": description,
                "files": files,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.post_body_multipart_response_200_files_item import PostBodyMultipartResponse200FilesItem

        d = dict(src_dict)
        a_string = d.pop("a_string")

        description = d.pop("description")

        files = []
        _files = d.pop("files")
        for files_item_data in _files:
            files_item = PostBodyMultipartResponse200FilesItem.from_dict(files_item_data)

            files.append(files_item)

        post_body_multipart_response_200 = cls(
            a_string=a_string,
            description=description,
            files=files,
        )

        post_body_multipart_response_200.additional_properties = d
        return post_body_multipart_response_200

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
