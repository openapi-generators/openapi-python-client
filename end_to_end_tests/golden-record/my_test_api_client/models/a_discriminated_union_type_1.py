from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from pydantic import ConfigDict, Field
from tandem_platform.schema.protected import BaseModel

T = TypeVar("T", bound="ADiscriminatedUnionType1")


class ADiscriminatedUnionType1(BaseModel):
    """
    Attributes:
        model_type (str | Unset):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    model_type: str | None = Field(default=None, alias="modelType")

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_unset=True, mode="json")

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)
