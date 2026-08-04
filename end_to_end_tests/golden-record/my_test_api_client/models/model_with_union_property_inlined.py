from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from pydantic import ConfigDict
from tandem_platform.schema.protected import BaseModel

if TYPE_CHECKING:
    from ..models.model_with_union_property_inlined_apples import ModelWithUnionPropertyInlinedApples
    from ..models.model_with_union_property_inlined_bananas import ModelWithUnionPropertyInlinedBananas


T = TypeVar("T", bound="ModelWithUnionPropertyInlined")


class ModelWithUnionPropertyInlined(BaseModel):
    """
    Attributes:
        fruit (ModelWithUnionPropertyInlinedApples | ModelWithUnionPropertyInlinedBananas | Unset):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    fruit: ModelWithUnionPropertyInlinedApples | ModelWithUnionPropertyInlinedBananas | None = None

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)


from ..models.model_with_union_property_inlined_apples import ModelWithUnionPropertyInlinedApples
from ..models.model_with_union_property_inlined_bananas import ModelWithUnionPropertyInlinedBananas

ModelWithUnionPropertyInlined.model_rebuild()
