from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from pydantic import ConfigDict
from tandem_platform.schema.protected import BaseModel

T = TypeVar("T", bound="ModelWithPrimitiveAdditionalProperties")


class ModelWithPrimitiveAdditionalProperties(BaseModel):
    """
    Attributes:
        a_date_holder (dict[str, datetime.datetime] | Unset):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    a_date_holder: dict[str, datetime.datetime] | None = None

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)
