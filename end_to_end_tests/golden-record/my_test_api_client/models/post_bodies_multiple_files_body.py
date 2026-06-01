from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from pydantic import ConfigDict
from tandem_platform.schema.protected import BaseModel

from .. import types

T = TypeVar("T", bound="PostBodiesMultipleFilesBody")


class PostBodiesMultipleFilesBody(BaseModel):
    """
    Attributes:
        a (str | Unset):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    a: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_unset=True, mode="json")

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        if "a" in self.model_fields_set and self.a is not None:
            files.append(("a", (None, str(self.a).encode(), "text/plain")))

        for prop_name, prop in (self.__pydantic_extra__ or {}).items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files
