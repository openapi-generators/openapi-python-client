from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from pydantic import ConfigDict
from tandem_platform.schema.protected import BaseModel

if TYPE_CHECKING:
    from ..models.an_object import AnObject
    from ..models.file import File


T = TypeVar("T", bound="PostBodyMultipartResponse200")


class PostBodyMultipartResponse200(BaseModel):
    """
    Attributes:
        a_string (str): Echo of the 'a_string' input parameter from the form.
        description (str): Echo of the 'description' input parameter from the form.
        files (list[File]):
        times (list[datetime.datetime]):
        objects (list[AnObject]):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    a_string: str
    description: str
    files: list[File]
    times: list[datetime.datetime]
    objects: list[AnObject]

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)


from ..models.an_object import AnObject
from ..models.file import File

PostBodyMultipartResponse200.model_rebuild(raise_errors=False)
