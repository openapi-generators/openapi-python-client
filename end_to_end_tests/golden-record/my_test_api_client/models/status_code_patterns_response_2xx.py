from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from pydantic import ConfigDict
from tandem_platform.schema.protected import BaseModel

from ..models.status_code_patterns_response_2xx_status import StatusCodePatternsResponse2XXStatus

T = TypeVar("T", bound="StatusCodePatternsResponse2XX")


class StatusCodePatternsResponse2XX(BaseModel):
    """
    Attributes:
        status (StatusCodePatternsResponse2XXStatus | Unset):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    status: StatusCodePatternsResponse2XXStatus | None = None

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_unset=True, mode="json")

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)
