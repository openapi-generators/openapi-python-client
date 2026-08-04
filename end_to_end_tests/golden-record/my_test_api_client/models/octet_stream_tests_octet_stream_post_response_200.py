from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from pydantic import ConfigDict
from tandem_platform.schema.protected import BaseModel

from ..types import File

T = TypeVar("T", bound="OctetStreamTestsOctetStreamPostResponse200")


class OctetStreamTestsOctetStreamPostResponse200(BaseModel):
    """
    Attributes:
        data (File | Unset):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    data: File | None = None

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)
