from __future__ import annotations

__all__ = ["PropertyProtocol", "Value", "convert_example"]

from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, ClassVar, Protocol, TypeVar

from ... import Config
from ... import schema as oai
from ...strings import PythonCode, PythonIdentifier, safe_for_docstring
from ..errors import ParseError, PropertyError


def convert_example(example: Any) -> oai.UntrustedString | None:
    """
    Convert a raw OpenAPI `example` (which can be anything) into an `UntrustedString` (or None).

    Examples only ever appear in docstrings, so non-string examples are stringified. Wrapping ensures a
    template which uses an example without escaping renders a safe-but-broken value instead of an exploit.
    """
    if example is None or isinstance(example, oai.UntrustedString):
        return example
    if isinstance(example, str):
        return oai.UntrustedString(example)
    return oai.UntrustedString(str(example))


@dataclass
class Value:
    """
    Some literal values in OpenAPI documents (like defaults) have to be converted into Python code safely
    (with string escaping, for example). We still keep the `raw_value` around for merging `allOf`.
    """

    python_code: PythonCode
    raw_value: Any


PropertyType = TypeVar("PropertyType", bound="PropertyProtocol")


class PropertyProtocol(Protocol):
    """
    Describes a single property for a schema

    Attributes:
        template: Name of the template file (if any) to use for this property. Must be stored in
            templates/property_templates and must contain two macros: construct and transform. Construct will be used to
            build this property from JSON data (a response from an API). Transform will be used to convert this property
            to JSON data (when sending a request to the API).

    Raises:
        ValidationError: Raised when the default value fails to be converted to the expected type
    """

    name: oai.UntrustedString
    required: bool
    _type_string: ClassVar[str] = ""
    _json_type_string: ClassVar[str] = ""  # Type of the property after JSON serialization
    _allowed_locations: ClassVar[set[oai.ParameterLocation]] = {
        oai.ParameterLocation.QUERY,
        oai.ParameterLocation.PATH,
        oai.ParameterLocation.COOKIE,
    }
    default: Value | None
    python_name: PythonIdentifier
    description: oai.UntrustedString | None
    example: oai.UntrustedString | None

    template: ClassVar[str] = "any_property.py.jinja"
    json_is_dict: ClassVar[bool] = False

    @abstractmethod
    def convert_value(self, value: Any) -> Value | PropertyError | None:
        """Convert a string value to a Value object"""
        raise NotImplementedError()  # pragma: no cover

    def validate_location(self, location: oai.ParameterLocation) -> ParseError | None:
        """Returns an error if this type of property is not allowed in the given location"""
        if location not in self._allowed_locations:
            return ParseError(detail=f"{self.get_type_string().as_unembedded_code()} is not allowed in {location}")
        if location == oai.ParameterLocation.PATH and not self.required:
            return ParseError(detail="Path parameter must be required")
        return None

    def set_python_name(self, new_name: oai.UntrustedString, config: Config, skip_snake_case: bool = False) -> None:
        """Mutates this Property to set a new python_name.

        Required to mutate due to how Properties are stored and the difficulty of updating them in-dict.
        `new_name` will be validated before it is set, so `python_name` is not guaranteed to equal `new_name` after
        calling this.
        """
        object.__setattr__(
            self,
            "python_name",
            PythonIdentifier(value=new_name, prefix=config.field_prefix, skip_snake_case=skip_snake_case),
        )

    def get_base_type_string(self) -> PythonCode:
        """Get the code describing the Python type of this property. Base types no require quoting."""
        return PythonCode(self._type_string)

    def get_base_json_type_string(self) -> PythonCode:
        """Get the code describing the JSON type of this property. Base types no require quoting."""
        return PythonCode(self._json_type_string)

    def get_type_string(
        self,
        no_optional: bool = False,
        json: bool = False,
    ) -> PythonCode:
        """
        Get a Python code representation of type that should be used when declaring this property

        Args:
            no_optional: Do not include Optional or Unset even if the value is optional (needed for isinstance checks)
            json: True if the type refers to the property after JSON serialization
        """
        if json:
            type_string = self.get_base_json_type_string()
        else:
            type_string = self.get_base_type_string()

        if no_optional or self.required:
            return type_string
        return PythonCode(f"{type_string.as_unembedded_code()} | Unset")

    def get_instance_type_string(self) -> PythonCode:
        """Get a Python code representation of runtime type that should be used for `isinstance` checks"""
        return self.get_type_string(no_optional=True)

    # noinspection PyUnusedLocal
    def get_imports(self, *, prefix: str) -> set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names. This should be the number of . to get
            back to the root of the generated client.
        """
        imports = set()
        if not self.required:
            imports.add(f"from {prefix}types import UNSET, Unset")
        return imports

    def get_lazy_imports(self, *, prefix: str) -> set[str]:
        """Get a set of lazy import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names. This should be the number of . to get
            back to the root of the generated client.
        """
        return set()

    def to_string(self) -> PythonCode:
        """How this should be declared in a dataclass"""
        default: str | None
        if self.default is not None:
            default = self.default.python_code.as_unembedded_code()
        elif not self.required:
            default = "UNSET"
        else:
            default = None

        declaration = f"{self.python_name}: {self.get_type_string().as_unembedded_code()}"
        if default is not None:
            declaration += f" = {default}"
        return PythonCode(declaration)

    def to_docstring(self) -> str:
        """Returns property docstring"""
        doc = f"{self.python_name} ({safe_for_docstring(self.get_type_string())}): {safe_for_docstring(self.description or '')}"
        if self.default:
            doc += f" Default: {safe_for_docstring(self.default.python_code)}."
        if self.example:
            doc += f" Example: {safe_for_docstring(self.example)}."
        return doc
