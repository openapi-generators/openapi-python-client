from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from pydantic import ConfigDict, Field
from tandem_platform.schema.protected import BaseModel

from ..models.another_all_of_sub_model_type import AnotherAllOfSubModelType
from ..models.another_all_of_sub_model_type_enum import AnotherAllOfSubModelTypeEnum

T = TypeVar("T", bound="ModelFromAllOf")


class ModelFromAllOf(BaseModel):
    """
    Attributes:
        a_sub_property (str | Unset):
        type_ (AnotherAllOfSubModelType | Unset):
        type_enum (AnotherAllOfSubModelTypeEnum | Unset):
        another_sub_property (str | Unset):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    a_sub_property: str | None = None
    type_: AnotherAllOfSubModelType | None = Field(default=None, alias="type")
    type_enum: AnotherAllOfSubModelTypeEnum | None = None
    another_sub_property: str | None = None

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)
