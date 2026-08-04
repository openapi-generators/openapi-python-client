from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from pydantic import ConfigDict
from tandem_platform.schema.protected import BaseModel

if TYPE_CHECKING:
    from ..models.an_array_with_a_circular_ref_in_items_object_a_item import AnArrayWithACircularRefInItemsObjectAItem


T = TypeVar("T", bound="AnArrayWithACircularRefInItemsObjectBItem")


class AnArrayWithACircularRefInItemsObjectBItem(BaseModel):
    """
    Attributes:
        circular (list[AnArrayWithACircularRefInItemsObjectAItem] | Unset):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    circular: list[AnArrayWithACircularRefInItemsObjectAItem] | None = None

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)


from ..models.an_array_with_a_circular_ref_in_items_object_a_item import AnArrayWithACircularRefInItemsObjectAItem

AnArrayWithACircularRefInItemsObjectBItem.model_rebuild(raise_errors=False)
