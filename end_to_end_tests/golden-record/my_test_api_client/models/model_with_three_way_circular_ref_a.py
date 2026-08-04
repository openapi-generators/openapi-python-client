from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from pydantic import ConfigDict
from tandem_platform.schema.protected import BaseModel

if TYPE_CHECKING:
    from ..models.model_with_three_way_circular_ref_b import ModelWithThreeWayCircularRefB


T = TypeVar("T", bound="ModelWithThreeWayCircularRefA")


class ModelWithThreeWayCircularRefA(BaseModel):
    """
    Attributes:
        circular (ModelWithThreeWayCircularRefB | Unset):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    circular: ModelWithThreeWayCircularRefB | None = None

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)


from ..models.model_with_three_way_circular_ref_b import ModelWithThreeWayCircularRefB

ModelWithThreeWayCircularRefA.model_rebuild(raise_errors=False)
