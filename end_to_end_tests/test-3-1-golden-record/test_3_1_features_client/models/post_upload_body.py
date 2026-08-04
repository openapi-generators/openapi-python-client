from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from pydantic import ConfigDict
from tandem_platform.schema.protected import BaseModel

from .. import types
from ..types import File

T = TypeVar("T", bound="PostUploadBody")


class PostUploadBody(BaseModel):
    """
    Attributes:
        file (File):
        files (list[File] | Unset):
        description (str | Unset):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    file: File
    files: list[File] | None = None
    description: str | None = None

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        files.append(("file", self.file.to_tuple()))

        if "files" in self.model_fields_set and self.files is not None:
            for files_item_element in self.files:
                files.append(("files", files_item_element.to_tuple()))

        if "description" in self.model_fields_set and self.description is not None:
            files.append(("description", (None, str(self.description).encode(), "text/plain")))

        for prop_name, prop in (self.__pydantic_extra__ or {}).items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files
