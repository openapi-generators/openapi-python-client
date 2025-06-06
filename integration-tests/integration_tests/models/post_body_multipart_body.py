import datetime
import json
from collections.abc import Mapping
from io import BytesIO
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from .. import types
from ..types import File

if TYPE_CHECKING:
    from ..models.an_object import AnObject


T = TypeVar("T", bound="PostBodyMultipartBody")


@_attrs_define
class PostBodyMultipartBody:
    """
    Attributes:
        a_string (str):
        files (list[File]):
        description (str):
        objects (list['AnObject']):
        times (list[datetime.datetime]):
    """

    a_string: str
    files: list[File]
    description: str
    objects: list["AnObject"]
    times: list[datetime.datetime]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        a_string = self.a_string

        files = []
        for files_item_data in self.files:
            files_item = files_item_data.to_tuple()

            files.append(files_item)

        description = self.description

        objects = []
        for objects_item_data in self.objects:
            objects_item = objects_item_data.to_dict()
            objects.append(objects_item)

        times = []
        for times_item_data in self.times:
            times_item = times_item_data.isoformat()
            times.append(times_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "a_string": a_string,
                "files": files,
                "description": description,
                "objects": objects,
                "times": times,
            }
        )

        return field_dict

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        files.append(("a_string", (None, str(self.a_string).encode(), "text/plain")))

        for files_item_element in self.files:
            files.append(("files", files_item_element.to_tuple()))

        files.append(("description", (None, str(self.description).encode(), "text/plain")))

        for objects_item_element in self.objects:
            files.append(("objects", (None, json.dumps(objects_item_element.to_dict()).encode(), "application/json")))

        for times_item_element in self.times:
            files.append(("times", (None, times_item_element.isoformat().encode(), "text/plain")))

        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.an_object import AnObject

        d = dict(src_dict)
        a_string = d.pop("a_string")

        files = []
        _files = d.pop("files")
        for files_item_data in _files:
            files_item = File(payload=BytesIO(files_item_data))

            files.append(files_item)

        description = d.pop("description")

        objects = []
        _objects = d.pop("objects")
        for objects_item_data in _objects:
            objects_item = AnObject.from_dict(objects_item_data)

            objects.append(objects_item)

        times = []
        _times = d.pop("times")
        for times_item_data in _times:
            times_item = isoparse(times_item_data)

            times.append(times_item)

        post_body_multipart_body = cls(
            a_string=a_string,
            files=files,
            description=description,
            objects=objects,
            times=times,
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
