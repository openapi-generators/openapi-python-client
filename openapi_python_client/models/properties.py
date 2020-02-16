from dataclasses import dataclass, field
from typing import Optional, List, Dict, Union, ClassVar

import stringcase

from .reference import Reference


@dataclass
class Property:
    """ Describes a single property for a schema """

    name: str
    required: bool
    default: Optional[str]

    _type_string: ClassVar[str]

    def get_type_string(self):
        """ Get a string representation of type that should be used when declaring this property """
        if self.required:
            return self._type_string
        return f"Optional[{self._type_string}]"

    def to_string(self) -> str:
        """ How this should be declared in a dataclass """
        if self.default:
            default = self.default
        elif not self.required:
            default = "None"
        else:
            default = None

        if default is not None:
            return f"{self.name}: {self.get_type_string()} = {self.default}"
        else:
            return f"{self.name}: {self.get_type_string()}"


@dataclass
class StringProperty(Property):
    """ A property of type str """

    max_length: Optional[int] = None
    pattern: Optional[str] = None

    _type_string: ClassVar[str] = "str"

    def __post_init__(self):
        if self.default is not None:
            self.default = f'"{self.default}"'


@dataclass
class DateTimeProperty(Property):
    """ A property of type datetime.datetime """

    _type_string: ClassVar[str] = "datetime"


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


@dataclass
class ListProperty(Property):
    """ Property for list """

    type: Optional[str]
    reference: Optional[Reference]

    def get_type_string(self):
        """ Get a string representation of type that should be used when declaring this property """
        if self.required:
            return f"List[{self.type}]"
        return f"Optional[List[{self.type}]]"


@dataclass
class EnumProperty(Property):
    """ A property that should use an enum """

    values: Dict[str, str]
    class_name: str = field(init=False)

    def __post_init__(self):
        self.class_name = stringcase.pascalcase(self.name)

    def get_type_string(self):
        """ Get a string representation of type that should be used when declaring this property """

        if self.required:
            return self.class_name
        return f"Optional[{self.class_name}]"

    @staticmethod
    def values_from_list(l: List[str], /) -> Dict[str, str]:
        """ Convert a list of values into dict of {name: value} """
        output: Dict[str, str] = {}

        for i, value in enumerate(l):
            if value.isalpha():
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

    def get_type_string(self):
        """ Get a string representation of type that should be used when declaring this property """
        if self.required:
            return self.reference.class_name
        return f"Optional[{self.reference.class_name}]"

    def to_string(self) -> str:
        """ How this should be declared in a dataclass """
        return f"{self.name}: {self.get_type_string()}"


@dataclass
class DictProperty(Property):
    """ Property that is a general Dict """

    _type_string: ClassVar[str] = "Dict"

    def to_string(self) -> str:
        """ How this should be declared in a dataclass """
        return f"{self.name}: {self.get_type_string()}"


_openapi_types_to_python_type_strings = {
    "string": "str",
    "number": "float",
    "integer": "int",
    "boolean": "bool",
    "object": "Dict",
}


def property_from_dict(
    name: str, required: bool, data: Dict[str, Union[float, int, str, List[str], Dict[str, str]]]
) -> Property:
    """ Generate a Property from the OpenAPI dictionary representation of it """
    if "enum" in data:
        return EnumProperty(
            name=name,
            required=required,
            values=EnumProperty.values_from_list(data["enum"]),
            default=data.get("default"),
        )
    if "$ref" in data:
        return RefProperty(name=name, required=required, reference=Reference(data["$ref"]), default=None)
    if data["type"] == "string":
        if "format" not in data:
            return StringProperty(
                name=name, default=data.get("default"), required=required, pattern=data.get("pattern"),
            )
        elif data["format"] == "date-time":
            return DateTimeProperty(name=name, required=required, default=data.get("default"))
    elif data["type"] == "number":
        return FloatProperty(name=name, default=data.get("default"), required=required)
    elif data["type"] == "integer":
        return IntProperty(name=name, default=data.get("default"), required=required)
    elif data["type"] == "boolean":
        return BooleanProperty(name=name, required=required, default=data.get("default"))
    elif data["type"] == "array":
        reference = None
        if "$ref" in data["items"]:
            reference = Reference(data["items"]["$ref"])
        _type = None
        if "type" in data["items"]:
            _type = _openapi_types_to_python_type_strings[data["items"]["type"]]
        return ListProperty(name=name, required=required, type=_type, reference=reference, default=None)
    elif data["type"] == "object":
        return DictProperty(name=name, required=required, default=None)
    raise ValueError(f"Did not recognize type of {data}")
