from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PostBodyMultipartResponse200")


@_attrs_define
class PostBodyMultipartResponse200:
    """
    Attributes:
        a_string (str): Echo of the 'a_string' input parameter from the form.
        file_data (str): Echo of content of the 'file' input parameter from the form.
        description (str): Echo of the 'description' input parameter from the form.
        file_name (str): The name of the file uploaded.
        file_content_type (str): The content type of the file uploaded.
    """

    a_string: str
    file_data: str
    description: str
    file_name: str
    file_content_type: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        a_string = self.a_string
        file_data = self.file_data
        description = self.description
        file_name = self.file_name
        file_content_type = self.file_content_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "a_string": a_string,
                "file_data": file_data,
                "description": description,
                "file_name": file_name,
                "file_content_type": file_content_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        a_string = d.pop("a_string")

        file_data = d.pop("file_data")

        description = d.pop("description")

        file_name = d.pop("file_name")

        file_content_type = d.pop("file_content_type")

        post_body_multipart_response_200 = cls(
            a_string=a_string,
            file_data=file_data,
            description=description,
            file_name=file_name,
            file_content_type=file_content_type,
        )

        post_body_multipart_response_200.additional_properties = d
        return post_body_multipart_response_200

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
