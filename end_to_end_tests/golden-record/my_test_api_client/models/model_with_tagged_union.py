from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Annotated, Any, TypeVar

from pydantic import ConfigDict, Field
from tandem_platform.schema.protected import BaseModel

if TYPE_CHECKING:
    from ..models.a_tagged_union_type_1 import ATaggedUnionType1
    from ..models.a_tagged_union_type_2 import ATaggedUnionType2


T = TypeVar("T", bound="ModelWithTaggedUnion")


class ModelWithTaggedUnion(BaseModel):
    """
    Attributes:
        tagged_union (ATaggedUnionType1 | ATaggedUnionType2):
        nullable_tagged_union (ATaggedUnionType1 | ATaggedUnionType2 | None | Unset):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    tagged_union: Annotated[ATaggedUnionType1 | ATaggedUnionType2, Field(discriminator="model_type")] = Field(
        alias="taggedUnion"
    )
    nullable_tagged_union: Annotated[
        ATaggedUnionType1 | ATaggedUnionType2 | None, Field(discriminator="model_type")
    ] = Field(default=None, alias="nullableTaggedUnion")

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)


from ..models.a_tagged_union_type_1 import ATaggedUnionType1
from ..models.a_tagged_union_type_2 import ATaggedUnionType2

ModelWithTaggedUnion.model_rebuild(raise_errors=False)
