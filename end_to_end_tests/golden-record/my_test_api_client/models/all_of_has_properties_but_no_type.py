from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from pydantic import ConfigDict, Field
from tandem_platform.schema.protected import BaseModel

from ..models.all_of_has_properties_but_no_type_type_enum import AllOfHasPropertiesButNoTypeTypeEnum

T = TypeVar("T", bound="AllOfHasPropertiesButNoType")


class AllOfHasPropertiesButNoType(BaseModel):
    """
    Attributes:
        a_sub_property (str | Unset):
        type_ (str | Unset):
        type_enum (AllOfHasPropertiesButNoTypeTypeEnum | Unset):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    a_sub_property: str | None = None
    type_: str | None = Field(default=None, alias="type")
    type_enum: AllOfHasPropertiesButNoTypeTypeEnum | None = None

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)
