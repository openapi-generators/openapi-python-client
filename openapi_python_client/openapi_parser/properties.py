from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Generic, List, Optional, Set, TypeVar, Union

from openapi_python_client import utils

from .reference import Reference


@dataclass
class Property:
    """
    Describes a single property for a schema

    Attributes:
        constructor_template: Name of the template file (if any) to use when constructing this property from JSON types.
    """

    name: str
    required: bool
    default: Optional[Any]

    constructor_template: ClassVar[Optional[str]] = None
    _type_string: ClassVar[str]

    python_name: str = field(init=False)

    def __post_init__(self) -> None:
        self.python_name = utils.snake_case(self.name)

    def get_type_string(self) -> str:
        """ Get a string representation of type that should be used when declaring this property """
        if self.required:
            return self._type_string
        return f"Optional[{self._type_string}]"

    def get_imports(self, *, prefix: str) -> Set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names.
        """
        if not self.required:
            return {"from typing import Optional"}
        return set()

    def to_string(self) -> str:
        """ How this should be declared in a dataclass """
        if self.default:
            default = self.default
        elif not self.required:
            default = "None"
        else:
            default = None

        if default is not None:
            return f"{self.python_name}: {self.get_type_string()} = {self.default}"
        else:
            return f"{self.python_name}: {self.get_type_string()}"

    def transform(self) -> str:
        """ What it takes to turn this object into a native python type """
        return self.python_name


@dataclass
class StringProperty(Property):
    """ A property of type str """

    max_length: Optional[int] = None
    pattern: Optional[str] = None

    _type_string: ClassVar[str] = "str"

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.default is not None:
            self.default = f'"{self.default}"'


@dataclass
class DateTimeProperty(Property):
    """
    A property of type datetime.datetime
    """

    _type_string: ClassVar[str] = "datetime"
    constructor_template: ClassVar[str] = "datetime_property.pyi"

    def transform(self) -> str:
        return f"{self.python_name}.isoformat()"

    def get_imports(self, *, prefix: str) -> Set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names.
        """
        imports = super().get_imports(prefix=prefix)
        imports.update(
            {"from datetime import datetime", "from typing import cast",}
        )
        return imports


@dataclass
class DateProperty(Property):
    """ A property of type datetime.date """

    _type_string: ClassVar[str] = "date"
    constructor_template: ClassVar[str] = "date_property.pyi"

    def transform(self) -> str:
        return f"{self.python_name}.isoformat()"

    def get_imports(self, *, prefix: str) -> Set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names.
        """
        imports = super().get_imports(prefix=prefix)
        imports.update(
            {"from datetime import date", "from typing import cast",}
        )
        return imports


@dataclass
class FileProperty(Property):
    """ A property used for uploading files """

    _type_string: ClassVar[str] = "File"

    def transform(self) -> str:
        return f"{self.python_name}.to_tuple()"

    def get_imports(self, *, prefix: str) -> Set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names.
        """
        imports = super().get_imports(prefix=prefix)
        imports.update({f"from {prefix}.types import File", "from dataclasses import astuple"})
        return imports


@dataclass
class FloatProperty(Property):
    """ A property of type float """

    default: Optional[float] = None
    _type_string: ClassVar[str] = "float"


@dataclass
class IntProperty(Property):
    """ A property of type int """

    default: Optional[int] = None
    _type_string: ClassVar[str] = "int"


@dataclass
class BooleanProperty(Property):
    """ Property for bool """

    _type_string: ClassVar[str] = "bool"


InnerProp = TypeVar("InnerProp", bound=Property)


@dataclass
class ListProperty(Property, Generic[InnerProp]):
    """ A property representing a list (array) of other properties """

    inner_property: InnerProp
    constructor_template: ClassVar[str] = "list_property.pyi"

    def get_type_string(self) -> str:
        """ Get a string representation of type that should be used when declaring this property """
        if self.required:
            return f"List[{self.inner_property.get_type_string()}]"
        return f"Optional[List[{self.inner_property.get_type_string()}]]"

    def get_imports(self, *, prefix: str) -> Set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names.
        """
        imports = super().get_imports(prefix=prefix)
        imports.update(self.inner_property.get_imports(prefix=prefix))
        imports.add("from typing import List")
        return imports


@dataclass
class EnumProperty(Property):
    """ A property that should use an enum """

    values: Dict[str, str]
    reference: Reference

    constructor_template: ClassVar[str] = "enum_property.pyi"

    def __post_init__(self) -> None:
        super().__post_init__()
        inverse_values = {v: k for k, v in self.values.items()}
        if self.default is not None:
            self.default = f"{self.reference.class_name}.{inverse_values[self.default]}"

    def get_type_string(self) -> str:
        """ Get a string representation of type that should be used when declaring this property """

        if self.required:
            return self.reference.class_name
        return f"Optional[{self.reference.class_name}]"

    def get_imports(self, *, prefix: str) -> Set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names.
        """
        imports = super().get_imports(prefix=prefix)
        imports.add(f"from {prefix}.{self.reference.module_name} import {self.reference.class_name}")
        return imports

    def transform(self) -> str:
        """ Output to the template, convert this Enum into a JSONable value """
        return f"{self.python_name}.value"

    @staticmethod
    def values_from_list(l: List[str], /) -> Dict[str, str]:
        """ Convert a list of values into dict of {name: value} """
        output: Dict[str, str] = {}

        for i, value in enumerate(l):
            if value[0].isalpha():
                key = value.upper()
            else:
                key = f"VALUE_{i}"
            assert key not in output, f"Duplicate key {key} in Enum"
            output[key] = value

        return output


@dataclass
class RefProperty(Property):
    """ A property which refers to another Schema """

    reference: Reference

    constructor_template: ClassVar[str] = "ref_property.pyi"

    def get_type_string(self) -> str:
        """ Get a string representation of type that should be used when declaring this property """
        if self.required:
            return self.reference.class_name
        return f"Optional[{self.reference.class_name}]"

    def get_imports(self, *, prefix: str) -> Set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names.
        """
        imports = super().get_imports(prefix=prefix)
        imports.update(
            {
                f"from {prefix}.{self.reference.module_name} import {self.reference.class_name}",
                "from typing import Dict",
                "from typing import cast",
            }
        )
        return imports

    def transform(self) -> str:
        """ Convert this into a JSONable value """
        return f"{self.python_name}.to_dict()"


@dataclass
class DictProperty(Property):
    """ Property that is a general Dict """

    _type_string: ClassVar[str] = "Dict[Any, Any]"

    def get_imports(self, *, prefix: str) -> Set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names.
        """
        imports = super().get_imports(prefix=prefix)
        imports.add("from typing import Dict")
        return imports


_openapi_types_to_python_type_strings = {
    "string": "str",
    "number": "float",
    "integer": "int",
    "boolean": "bool",
    "object": "Dict[Any, Any]",
}


def _string_based_property(
    name: str, required: bool, data: Dict[str, Any]
) -> Union[StringProperty, DateProperty, DateTimeProperty, FileProperty]:
    """ Construct a Property from the type "string" """
    string_format = data.get("format")
    if string_format is None:
        return StringProperty(name=name, default=data.get("default"), required=required, pattern=data.get("pattern"))
    if string_format == "date-time":
        return DateTimeProperty(name=name, required=required, default=data.get("default"))
    elif string_format == "date":
        return DateProperty(name=name, required=required, default=data.get("default"))
    elif string_format == "binary":
        return FileProperty(name=name, required=required, default=data.get("default"))
    else:
        raise ValueError(f'Unsupported string format:{data["format"]}')


def property_from_dict(name: str, required: bool, data: Dict[str, Any]) -> Property:
    """ Generate a Property from the OpenAPI dictionary representation of it """
    if "enum" in data:
        return EnumProperty(
            name=name,
            required=required,
            values=EnumProperty.values_from_list(data["enum"]),
            reference=Reference.from_ref(data.get("title", name)),
            default=data.get("default"),
        )
    if "$ref" in data:
        return RefProperty(name=name, required=required, reference=Reference.from_ref(data["$ref"]), default=None)
    if data["type"] == "string":
        return _string_based_property(name=name, required=required, data=data)
    elif data["type"] == "number":
        return FloatProperty(name=name, default=data.get("default"), required=required)
    elif data["type"] == "integer":
        return IntProperty(name=name, default=data.get("default"), required=required)
    elif data["type"] == "boolean":
        return BooleanProperty(name=name, required=required, default=data.get("default"))
    elif data["type"] == "array":
        return ListProperty(
            name=name,
            required=required,
            default=None,
            inner_property=property_from_dict(name=f"{name}_item", required=True, data=data["items"]),
        )
    elif data["type"] == "object":
        return DictProperty(name=name, required=required, default=data.get("default"))
    raise ValueError(f"Did not recognize type of {data}")
