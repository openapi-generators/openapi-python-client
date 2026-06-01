from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from pydantic import ConfigDict, Field
from tandem_platform.schema.protected import BaseModel

T = TypeVar("T", bound="PostNamingPropertyConflictWithImportBody")


class PostNamingPropertyConflictWithImportBody(BaseModel):
    """
    Attributes:
        field (str | Unset): A python_name of field should not interfere with attrs field
        define (str | Unset): A python_name of define should not interfere with attrs define
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    field: str | None = Field(default=None, alias="Field")
    define: str | None = Field(default=None, alias="Define")

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_unset=True, mode="json")

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)
