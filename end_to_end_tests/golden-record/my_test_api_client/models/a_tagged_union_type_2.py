from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar

from pydantic import ConfigDict, Field
from tandem_platform.schema.protected import BaseModel

T = TypeVar("T", bound="ATaggedUnionType2")


class ATaggedUnionType2(BaseModel):
    """
    Attributes:
        model_type (Literal['type2']):
        texture (str | Unset):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    model_type: Literal["type2"] = Field(alias="modelType")
    texture: str | None = None

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)
