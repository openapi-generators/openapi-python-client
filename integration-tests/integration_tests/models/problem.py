from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from pydantic import ConfigDict
from tandem_platform.schema.protected import BaseModel

T = TypeVar("T", bound="Problem")


class Problem(BaseModel):
    """
    Attributes:
        parameter_name (str | Unset):
        description (str | Unset):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    parameter_name: str | None = None
    description: str | None = None

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)
