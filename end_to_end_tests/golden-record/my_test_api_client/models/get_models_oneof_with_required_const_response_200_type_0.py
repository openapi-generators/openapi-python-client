from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar

from pydantic import ConfigDict, Field
from tandem_platform.schema.protected import BaseModel

T = TypeVar("T", bound="GetModelsOneofWithRequiredConstResponse200Type0")


class GetModelsOneofWithRequiredConstResponse200Type0(BaseModel):
    """
    Attributes:
        type_ (Literal['alpha']):
        color (str | Unset):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    type_: Literal["alpha"] = Field(alias="type")
    color: str | None = None

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)
