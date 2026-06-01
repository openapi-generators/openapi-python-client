from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from pydantic import ConfigDict, Field
from tandem_platform.schema.protected import BaseModel

from ..models.model_with_merged_properties_string_to_enum import ModelWithMergedPropertiesStringToEnum

T = TypeVar("T", bound="ModelWithMergedProperties")


class ModelWithMergedProperties(BaseModel):
    """
    Attributes:
        simple_string (str | Unset): extended simpleString description Default: 'new default'.
        string_to_enum (ModelWithMergedPropertiesStringToEnum | Unset):  Default:
            ModelWithMergedPropertiesStringToEnum.A.
        string_to_date (datetime.date | Unset):
        number_to_int (int | Unset):
        any_to_string (str | Unset):  Default: 'x'.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    simple_string: str | None = Field(default="new default", alias="simpleString")
    string_to_enum: ModelWithMergedPropertiesStringToEnum | None = Field(
        default=ModelWithMergedPropertiesStringToEnum.A, alias="stringToEnum"
    )
    string_to_date: datetime.date | None = Field(default=None, alias="stringToDate")
    number_to_int: int | None = Field(default=None, alias="numberToInt")
    any_to_string: str | None = Field(default="x", alias="anyToString")

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_unset=True, mode="json")

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)
