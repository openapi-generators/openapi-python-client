from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from pydantic import ConfigDict
from tandem_platform.schema.protected import BaseModel

T = TypeVar("T", bound="AFormData")


class AFormData(BaseModel):
    """
    Attributes:
        an_required_field (str):
        an_optional_field (str | Unset):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    an_required_field: str
    an_optional_field: str | None = None

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)
