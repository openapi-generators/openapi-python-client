from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from pydantic import ConfigDict, Field
from tandem_platform.schema.protected import BaseModel

from ..models.all_of_sub_model_type_enum import AllOfSubModelTypeEnum

T = TypeVar("T", bound="AllOfSubModel")


class AllOfSubModel(BaseModel):
    """
    Attributes:
        a_sub_property (str | Unset):
        type_ (str | Unset):
        type_enum (AllOfSubModelTypeEnum | Unset):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    a_sub_property: str | None = None
    type_: str | None = Field(default=None, alias="type")
    type_enum: AllOfSubModelTypeEnum | None = None

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_unset=True, mode="json")

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)
