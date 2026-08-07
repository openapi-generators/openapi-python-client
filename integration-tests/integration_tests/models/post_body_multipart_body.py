from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from pydantic import ConfigDict
from tandem_platform.schema.protected import BaseModel

from .. import types
from ..types import File

if TYPE_CHECKING:
    from ..models.an_object import AnObject


T = TypeVar("T", bound="PostBodyMultipartBody")


class PostBodyMultipartBody(BaseModel):
    """
    Attributes:
        a_string (str):
        files (list[File]):
        description (str):
        objects (list[AnObject]):
        times (list[datetime.datetime]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    a_string: str
    files: list[File]
    description: str
    objects: list[AnObject]
    times: list[datetime.datetime]

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        files.append(("a_string", (None, str(self.a_string).encode(), "text/plain")))

        for files_item_element in self.files:
            files.append(("files", files_item_element.to_tuple()))

        files.append(("description", (None, str(self.description).encode(), "text/plain")))

        for objects_item_element in self.objects:
            files.append(("objects", (None, types.dump_json__for_transport(objects_item_element), "application/json")))

        for times_item_element in self.times:
            files.append(("times", (None, times_item_element.isoformat().encode(), "text/plain")))

        for prop_name, prop in (self.__pydantic_extra__ or {}).items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files


from ..models.an_object import AnObject

PostBodyMultipartBody.model_rebuild(raise_errors=False)
