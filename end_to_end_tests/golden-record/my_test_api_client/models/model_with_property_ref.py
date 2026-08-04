from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from pydantic import ConfigDict
from tandem_platform.schema.protected import BaseModel

if TYPE_CHECKING:
    from ..models.model_name import ModelName


T = TypeVar("T", bound="ModelWithPropertyRef")


class ModelWithPropertyRef(BaseModel):
    """
    Attributes:
        inner (ModelName | Unset):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    inner: ModelName | None = None

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)


from ..models.model_name import ModelName

ModelWithPropertyRef.model_rebuild()
