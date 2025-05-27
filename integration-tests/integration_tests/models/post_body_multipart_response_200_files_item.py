from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostBodyMultipartResponse200FilesItem")


@_attrs_define
class PostBodyMultipartResponse200FilesItem:
    """
    Attributes:
        data (Union[Unset, str]): Echo of content of the 'file' input parameter from the form.
        name (Union[Unset, str]): The name of the file uploaded.
        content_type (Union[Unset, str]): The content type of the file uploaded.
    """

    data: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    content_type: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data

        name = self.name

        content_type = self.content_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data is not UNSET:
            field_dict["data"] = data
        if name is not UNSET:
            field_dict["name"] = name
        if content_type is not UNSET:
            field_dict["content_type"] = content_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        data = d.pop("data", UNSET)

        name = d.pop("name", UNSET)

        content_type = d.pop("content_type", UNSET)

        post_body_multipart_response_200_files_item = cls(
            data=data,
            name=name,
            content_type=content_type,
        )

        post_body_multipart_response_200_files_item.additional_properties = d
        return post_body_multipart_response_200_files_item

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
