from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from pydantic import ConfigDict, Field
from tandem_platform.schema.protected import BaseModel

T = TypeVar("T", bound="ModelWithDescription")


class ModelWithDescription(BaseModel):
    """This is a nice model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    prop_with_no_desc: str | None = Field(default=None, alias="propWithNoDesc")
    prop_with_desc: str | None = Field(default=None, alias="propWithDesc")
    """ This is a nice property. """
    prop_with_long_desc: str | None = Field(default=None, alias="propWithLongDesc")
    """ It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of
    foolishness,
    it was the epoch of belief, it was the epoch of incredulity, it was the season of light, it was the season of
    darkness, it was the spring of hope, it was the winter of despair.
     """

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_unset=True, mode="json")

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)
