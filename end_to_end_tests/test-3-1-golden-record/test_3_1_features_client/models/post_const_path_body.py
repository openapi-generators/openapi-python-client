from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar

from pydantic import ConfigDict
from tandem_platform.schema.protected import BaseModel

T = TypeVar("T", bound="PostConstPathBody")


class PostConstPathBody(BaseModel):
    """
    Attributes:
        required (Literal['this always goes in the body']):
        nullable (Literal['this or null goes in the body'] | None):
        optional (Literal['this sometimes goes in the body'] | Unset):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    required: Literal["this always goes in the body"]
    nullable: Literal["this or null goes in the body"] | None
    optional: Literal["this sometimes goes in the body"] | None = None

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)
