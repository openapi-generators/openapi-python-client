from __future__ import annotations

from typing import Any, ClassVar

from attr import define

from ... import utils
from ..errors import PropertyError
from .protocol import PropertyProtocol, Value


@define
class JsonlProperty(PropertyProtocol):
    """A property representing a JSONL (JSON Lines) response, parsed into a list of items"""

    name: str
    required: bool
    default: Value | None
    python_name: utils.PythonIdentifier
    description: str | None
    example: str | None
    inner_property: PropertyProtocol
    template: ClassVar[str] = "jsonl_property.py.jinja"

    def convert_value(self, value: Any) -> Value | None | PropertyError:
        return None  # pragma: no cover

    def get_base_type_string(self) -> str:
        return f"list[{self.inner_property.get_type_string()}]"

    def get_base_json_type_string(self) -> str:
        return f"list[{self.inner_property.get_type_string(json=True)}]"

    def get_instance_type_string(self) -> str:
        """Get a string representation of runtime type that should be used for `isinstance` checks"""
        return "list"

    def get_imports(self, *, prefix: str) -> set[str]:
        imports = super().get_imports(prefix=prefix)
        imports.update(self.inner_property.get_imports(prefix=prefix))
        imports.add("import orjson")
        imports.add("from collections.abc import Generator, AsyncGenerator")
        return imports

    def get_lazy_imports(self, *, prefix: str) -> set[str]:
        lazy_imports = super().get_lazy_imports(prefix=prefix)
        lazy_imports.update(self.inner_property.get_lazy_imports(prefix=prefix))
        return lazy_imports
