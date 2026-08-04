from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from pydantic import ConfigDict
from tandem_platform.schema.protected import BaseModel

if TYPE_CHECKING:
    from ..models.an_array_with_a_circular_ref_in_items_object_b_item import AnArrayWithACircularRefInItemsObjectBItem


T = TypeVar("T", bound="AnArrayWithACircularRefInItemsObjectAItem")


class AnArrayWithACircularRefInItemsObjectAItem(BaseModel):
    """
    Attributes:
        circular (list[AnArrayWithACircularRefInItemsObjectBItem] | Unset):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    circular: list[AnArrayWithACircularRefInItemsObjectBItem] | None = None

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)


from ..models.an_array_with_a_circular_ref_in_items_object_b_item import AnArrayWithACircularRefInItemsObjectBItem

AnArrayWithACircularRefInItemsObjectAItem.model_rebuild()
