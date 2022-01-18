from io import BytesIO
from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, File, Unset

T = TypeVar("T", bound="PostBodyMultipartMultipartData")


@attr.s(auto_attribs=True)
class PostBodyMultipartMultipartData:
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
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        a_string = self.a_string
        file = self.file.to_tuple()

        description = self.description

        field_dict: Dict[str, Any] = {}
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

    def to_multipart(self) -> Dict[str, Any]:
        a_string = (
            self.a_string if isinstance(self.a_string, Unset) else (None, str(self.a_string).encode(), "text/plain")
        )
        file = self.file.to_tuple()

        description = (
            self.description
            if isinstance(self.description, Unset)
            else (None, str(self.description).encode(), "text/plain")
        )

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {key: (None, str(value).encode(), "text/plain") for key, value in self.additional_properties.items()}
        )
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
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        a_string = d.pop("a_string")

        file = File(payload=BytesIO(d.pop("file")))

        description = d.pop("description", UNSET)

        post_body_multipart_multipart_data = cls(
            a_string=a_string,
            file=file,
            description=description,
        )

        post_body_multipart_multipart_data.additional_properties = d
        return post_body_multipart_multipart_data

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
