from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from pydantic import ConfigDict
from tandem_platform.schema.protected import BaseModel

if TYPE_CHECKING:
    from ..models.validation_error import ValidationError


T = TypeVar("T", bound="HTTPValidationError")


class HTTPValidationError(BaseModel):
    """
    Attributes:
        detail (list[ValidationError] | Unset):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    detail: list[ValidationError] | None = None

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)


from ..models.validation_error import ValidationError

HTTPValidationError.model_rebuild(raise_errors=False)
