from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from pydantic import ConfigDict
from tandem_platform.schema.protected import BaseModel

if TYPE_CHECKING:
    from ..models.post_responses_unions_simple_before_complex_response_200a_type_1 import (
        PostResponsesUnionsSimpleBeforeComplexResponse200AType1,
    )


T = TypeVar("T", bound="PostResponsesUnionsSimpleBeforeComplexResponse200")


class PostResponsesUnionsSimpleBeforeComplexResponse200(BaseModel):
    """
    Attributes:
        a (PostResponsesUnionsSimpleBeforeComplexResponse200AType1 | str):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    a: PostResponsesUnionsSimpleBeforeComplexResponse200AType1 | str

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)


from ..models.post_responses_unions_simple_before_complex_response_200a_type_1 import (
    PostResponsesUnionsSimpleBeforeComplexResponse200AType1,
)

PostResponsesUnionsSimpleBeforeComplexResponse200.model_rebuild()
