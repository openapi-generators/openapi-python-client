"""Shim of ``tandem_platform.schema.protected``.

Generated clients reference three symbols from this module (verified against the
golden records):

* ``BaseModel`` — the default base class for every generated model.
* ``ProtectedModel`` — base class for models flagged via a
  ``brand::protected::*`` schema ``format``.
* ``ProtectedString`` — field type for ``brand::protected::ProtectedString``.

The real package adds protection semantics; for testing we only need objects that
behave like plain Pydantic models / a string subtype so that generated code
imports, validates, round-trips, and type-checks under ``mypy --strict``.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel as _PydanticBaseModel
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema

__all__ = ["BaseModel", "ProtectedModel", "ProtectedString"]


class BaseModel(_PydanticBaseModel):
    """Default base for generated models."""


class ProtectedModel(_PydanticBaseModel):
    """Base for models whose schema ``format`` is ``brand::protected::<Name>``."""


class ProtectedString(str):
    """String subtype used for ``brand::protected::ProtectedString`` fields."""

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        """Make the shim usable as a field type, as the real package's hook does."""
        return core_schema.no_info_after_validator_function(cls, core_schema.str_schema())
