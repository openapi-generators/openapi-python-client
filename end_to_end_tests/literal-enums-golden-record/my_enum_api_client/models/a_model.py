from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from pydantic import ConfigDict
from tandem_platform.schema.protected import BaseModel

from ..models.an_all_of_enum import AnAllOfEnum
from ..models.an_enum import AnEnum
from ..models.different_enum import DifferentEnum

T = TypeVar("T", bound="AModel")


class AModel(BaseModel):
    """A Model for testing all the ways enums can be used

    Attributes:
        an_enum_value (AnEnum): For testing Enums in all the ways they can be used
        an_allof_enum_with_overridden_default (AnAllOfEnum):  Default: 'overridden_default'.
        any_value (Any | Unset):
        an_optional_allof_enum (AnAllOfEnum | Unset):
        nested_list_of_enums (list[list[DifferentEnum]] | Unset):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    an_enum_value: AnEnum
    an_allof_enum_with_overridden_default: AnAllOfEnum = "overridden_default"
    any_value: Any | None = None
    an_optional_allof_enum: AnAllOfEnum | None = None
    nested_list_of_enums: list[list[DifferentEnum]] | None = None

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_unset=True, mode="json")

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)
