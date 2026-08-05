from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar

from pydantic import ConfigDict, Field
from tandem_platform.schema.protected import BaseModel

T = TypeVar("T", bound="ATaggedUnionType1")


class ATaggedUnionType1(BaseModel):
    """
    Attributes:
        model_type (Literal['type1']):
        colour (str | Unset):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    model_type: Literal["type1"] = Field(alias="modelType")
    colour: str | None = None

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)
