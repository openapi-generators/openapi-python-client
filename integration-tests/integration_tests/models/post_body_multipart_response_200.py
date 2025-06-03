import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.an_object import AnObject
    from ..models.file import File


T = TypeVar("T", bound="PostBodyMultipartResponse200")


@_attrs_define
class PostBodyMultipartResponse200:
    """
    Attributes:
        a_string (str): Echo of the 'a_string' input parameter from the form.
        description (str): Echo of the 'description' input parameter from the form.
        files (list['File']):
        times (list[datetime.datetime]):
        objects (list['AnObject']):
    """

    a_string: str
    description: str
    files: list["File"]
    times: list[datetime.datetime]
    objects: list["AnObject"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        a_string = self.a_string

        description = self.description

        files = []
        for files_item_data in self.files:
            files_item = files_item_data.to_dict()
            files.append(files_item)

        times = []
        for times_item_data in self.times:
            times_item = times_item_data.isoformat()
            times.append(times_item)

        objects = []
        for objects_item_data in self.objects:
            objects_item = objects_item_data.to_dict()
            objects.append(objects_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "a_string": a_string,
                "description": description,
                "files": files,
                "times": times,
                "objects": objects,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.an_object import AnObject
        from ..models.file import File

        d = dict(src_dict)
        a_string = d.pop("a_string")

        description = d.pop("description")

        files = []
        _files = d.pop("files")
        for files_item_data in _files:
            files_item = File.from_dict(files_item_data)

            files.append(files_item)

        times = []
        _times = d.pop("times")
        for times_item_data in _times:
            times_item = isoparse(times_item_data)

            times.append(times_item)

        objects = []
        _objects = d.pop("objects")
        for objects_item_data in _objects:
            objects_item = AnObject.from_dict(objects_item_data)

            objects.append(objects_item)

        post_body_multipart_response_200 = cls(
            a_string=a_string,
            description=description,
            files=files,
            times=times,
            objects=objects,
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
