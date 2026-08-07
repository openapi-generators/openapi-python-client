from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from pydantic import ConfigDict
from tandem_platform.schema.protected import BaseModel

if TYPE_CHECKING:
    from ..models.problem import Problem


T = TypeVar("T", bound="PublicError")


class PublicError(BaseModel):
    """
    Attributes:
        errors (list[str] | Unset):
        extra_parameters (list[str] | Unset):
        invalid_parameters (list[Problem] | Unset):
        missing_parameters (list[str] | Unset):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    errors: list[str] | None = None
    extra_parameters: list[str] | None = None
    invalid_parameters: list[Problem] | None = None
    missing_parameters: list[str] | None = None

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)


from ..models.problem import Problem

PublicError.model_rebuild(raise_errors=False)
