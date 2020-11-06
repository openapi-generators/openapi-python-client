from dataclasses import dataclass, field
from typing import Any, ClassVar, Optional, Set

from ... import utils
from ..errors import ValidationError


@dataclass
class Property:
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

    name: str
    required: bool
    nullable: bool
    default: Optional[Any]

    template: ClassVar[Optional[str]] = None
    _type_string: ClassVar[str]

    python_name: str = field(init=False)

    def __post_init__(self) -> None:
        self.python_name = utils.to_valid_python_identifier(utils.snake_case(self.name))
        if self.default is not None:
            self.default = self._validate_default(default=self.default)

    def _validate_default(self, default: Any) -> Any:
        """ Check that the default value is valid for the property's type + perform any necessary sanitization """
        raise ValidationError

    def get_type_string(self, no_optional: bool = False) -> str:
        """
        Get a string representation of type that should be used when declaring this property

        Args:
            no_optional: Do not include Optional or Unset even if the value is optional (needed for isinstance checks)
        """
        type_string = self._type_string
        if no_optional:
            return self._type_string
        if self.nullable:
            type_string = f"Optional[{type_string}]"
        if not self.required:
            type_string = f"Union[Unset, {type_string}]"
        return type_string

    # noinspection PyUnusedLocal
    def get_imports(self, *, prefix: str) -> Set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names. This should be the number of . to get
            back to the root of the generated client.
        """
        imports = set()
        if self.nullable:
            imports.add("from typing import Optional")
        if not self.required:
            imports.add("from typing import Union")
            imports.add(f"from {prefix}types import UNSET, Unset")
        return imports

    def to_string(self) -> str:
        """ How this should be declared in a dataclass """
        if self.default:
            default = self.default
        elif not self.required:
            default = "UNSET"
        else:
            default = None

        if default is not None:
            return f"{self.python_name}: {self.get_type_string()} = {default}"
        else:
            return f"{self.python_name}: {self.get_type_string()}"
