from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar

from pydantic import ConfigDict, Field
from tandem_platform.schema.protected import BaseModel

T = TypeVar("T", bound="PostPrefixItemsBody")


class PostPrefixItemsBody(BaseModel):
    """
    Attributes:
        prefix_items_and_items (list[float | Literal['prefix'] | str] | Unset):
        prefix_items_only (list[float | str] | Unset):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    prefix_items_and_items: list[float | Literal["prefix"] | str] | None = Field(
        default=None, alias="prefixItemsAndItems"
    )
    prefix_items_only: list[float | str] | None = Field(default=None, alias="prefixItemsOnly")

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_unset=True, mode="json")

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)
