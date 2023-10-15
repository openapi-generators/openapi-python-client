from __future__ import annotations

from typing import ClassVar

from attr import define

from ...utils import PythonIdentifier
from .protocol import PropertyProtocol, Value


@define
class FileProperty(PropertyProtocol):
    """A property used for uploading files"""

    name: str
    required: bool
    default: Value | None
    python_name: PythonIdentifier
    description: str | None
    example: str | None

    _type_string: ClassVar[str] = "File"
    # Return type of File.to_tuple()
    _json_type_string: ClassVar[str] = "FileJsonType"
    template: ClassVar[str] = "file_property.py.jinja"

    @classmethod
    def build(
        cls,
        name: str,
        required: bool,
        default: str | Value | None,
        python_name: PythonIdentifier,
        description: str | None,
        example: str | None,
    ) -> FileProperty:
        return cls(
            name=name,
            required=required,
            default=cls.convert_value(default),
            python_name=python_name,
            description=description,
            example=example,
        )

    @classmethod
    def convert_value(cls, value: str | Value | None) -> Value | None:
        if isinstance(value, str):
            return Value(value)
        return value

    def get_imports(self, *, prefix: str) -> set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names. This should be the number of . to get
            back to the root of the generated client.
        """
        imports = super().get_imports(prefix=prefix)
        imports.update({f"from {prefix}types import File, FileJsonType", "from io import BytesIO"})
        return imports
