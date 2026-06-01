from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from pydantic import ConfigDict
from tandem_platform.schema.protected import BaseModel

if TYPE_CHECKING:
    pass


T = TypeVar("T", bound="ModelWithCircularRefInAdditionalPropertiesA")


class ModelWithCircularRefInAdditionalPropertiesA(BaseModel):
    """ """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_unset=True, mode="json")

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)


ModelWithCircularRefInAdditionalPropertiesA.model_rebuild()
