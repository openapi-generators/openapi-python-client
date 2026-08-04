from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from pydantic import ConfigDict
from tandem_platform.schema.protected import BaseModel

if TYPE_CHECKING:
    from ..models.model_with_three_way_circular_ref_a import ModelWithThreeWayCircularRefA


T = TypeVar("T", bound="ModelWithThreeWayCircularRefC")


class ModelWithThreeWayCircularRefC(BaseModel):
    """
    Attributes:
        circular (ModelWithThreeWayCircularRefA | Unset):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    circular: ModelWithThreeWayCircularRefA | None = None

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)


from ..models.model_with_three_way_circular_ref_a import ModelWithThreeWayCircularRefA

ModelWithThreeWayCircularRefC.model_rebuild(raise_errors=False)
