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

from pydantic import BaseModel as _PydanticBaseModel

__all__ = ["BaseModel", "ProtectedModel", "ProtectedString"]


class BaseModel(_PydanticBaseModel):
    """Default base for generated models."""


class ProtectedModel(_PydanticBaseModel):
    """Base for models whose schema ``format`` is ``brand::protected::<Name>``."""


class ProtectedString(str):
    """String subtype used for ``brand::protected::ProtectedString`` fields."""
