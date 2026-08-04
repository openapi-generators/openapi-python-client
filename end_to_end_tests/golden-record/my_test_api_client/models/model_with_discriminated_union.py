from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from pydantic import ConfigDict
from tandem_platform.schema.protected import BaseModel

if TYPE_CHECKING:
    from ..models.a_discriminated_union_type_1 import ADiscriminatedUnionType1
    from ..models.a_discriminated_union_type_2 import ADiscriminatedUnionType2


T = TypeVar("T", bound="ModelWithDiscriminatedUnion")


class ModelWithDiscriminatedUnion(BaseModel):
    """
    Attributes:
        discriminated_union (ADiscriminatedUnionType1 | ADiscriminatedUnionType2 | None | Unset):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    discriminated_union: ADiscriminatedUnionType1 | ADiscriminatedUnionType2 | None = None

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)


from ..models.a_discriminated_union_type_1 import ADiscriminatedUnionType1
from ..models.a_discriminated_union_type_2 import ADiscriminatedUnionType2

ModelWithDiscriminatedUnion.model_rebuild()
