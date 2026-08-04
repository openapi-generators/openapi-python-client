from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from pydantic import ConfigDict
from tandem_platform.schema.protected import BaseModel

T = TypeVar("T", bound="StatusCodePatternsResponse4XX")


class StatusCodePatternsResponse4XX(BaseModel):
    """
    Attributes:
        error (str | Unset):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    error: str | None = None

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)
