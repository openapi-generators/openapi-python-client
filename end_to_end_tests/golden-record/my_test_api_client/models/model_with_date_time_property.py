from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from pydantic import ConfigDict, Field
from tandem_platform.schema.protected import BaseModel

T = TypeVar("T", bound="ModelWithDateTimeProperty")


class ModelWithDateTimeProperty(BaseModel):
    """
    Attributes:
        datetime_ (datetime.datetime | Unset):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    datetime_: datetime.datetime | None = Field(default=None, alias="datetime")

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)
