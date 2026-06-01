from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from pydantic import ConfigDict
from tandem_platform.schema.protected import BaseModel

from ..models.an_enum import AnEnum
from ..models.an_int_enum import AnIntEnum

T = TypeVar("T", bound="ModelWithUnionProperty")


class ModelWithUnionProperty(BaseModel):
    """
    Attributes:
        a_property (AnEnum | AnIntEnum | Unset):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    a_property: AnEnum | AnIntEnum | None = None

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_unset=True, mode="json")

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)
