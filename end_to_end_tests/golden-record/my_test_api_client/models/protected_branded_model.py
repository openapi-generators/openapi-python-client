from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from pydantic import ConfigDict
from tandem_platform.schema.protected import ProtectedModel, ProtectedString

T = TypeVar("T", bound="ProtectedBrandedModel")


class ProtectedBrandedModel(ProtectedModel):
    """
    Attributes:
        protected_field (ProtectedString):
        public_field (str):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    protected_field: ProtectedString
    public_field: str

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)
