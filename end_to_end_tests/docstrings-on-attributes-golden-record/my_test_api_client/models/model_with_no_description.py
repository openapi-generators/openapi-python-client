from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from pydantic import ConfigDict, Field
from tandem_platform.schema.protected import BaseModel

T = TypeVar("T", bound="ModelWithNoDescription")


class ModelWithNoDescription(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    prop_with_no_desc: str | None = Field(default=None, alias="propWithNoDesc")
    prop_with_desc: str | None = Field(default=None, alias="propWithDesc")
    """ This is a nice property. """

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)
