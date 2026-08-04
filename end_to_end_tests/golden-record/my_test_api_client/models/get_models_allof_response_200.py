from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from pydantic import ConfigDict
from tandem_platform.schema.protected import BaseModel

if TYPE_CHECKING:
    from ..models.a_model import AModel
    from ..models.extended import Extended


T = TypeVar("T", bound="GetModelsAllofResponse200")


class GetModelsAllofResponse200(BaseModel):
    """
    Attributes:
        aliased (AModel | Unset): A Model for testing all the ways custom objects can be used
        extended (Extended | Unset):
        model (AModel | Unset): A Model for testing all the ways custom objects can be used
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    aliased: AModel | None = None
    extended: Extended | None = None
    model: AModel | None = None

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)


from ..models.a_model import AModel
from ..models.extended import Extended

GetModelsAllofResponse200.model_rebuild()
