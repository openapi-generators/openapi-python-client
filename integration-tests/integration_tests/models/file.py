from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from pydantic import ConfigDict
from tandem_platform.schema.protected import BaseModel

T = TypeVar("T", bound="File")


class File(BaseModel):
    """
    Attributes:
        data (str | Unset): Echo of content of the 'file' input parameter from the form.
        name (str | Unset): The name of the file uploaded.
        content_type (str | Unset): The content type of the file uploaded.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    data: str | None = None
    name: str | None = None
    content_type: str | None = None

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)
