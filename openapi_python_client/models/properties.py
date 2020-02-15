from dataclasses import dataclass, field
from typing import Optional, List, Dict, Union, ClassVar
import stringcase


@dataclass
class Property:
    """ Describes a single property for a schema """

    name: str
    required: bool

    _type_string: ClassVar[str]

    def get_type_string(self):
        """ Get a string representation of type that should be used when declaring this property """
        if self.required:
            return self._type_string
        return f"Optional[{self._type_string}]"


@dataclass
class StringProperty(Property):
    """ A property of type str """

    max_length: Optional[int] = None
    default: Optional[str] = None
    pattern: Optional[str] = None

    _type_string: ClassVar[str] = "str"

    def to_string(self) -> str:
        """ How this should be declared in a dataclass """
        if self.default:
            return f"{self.name}: {self.get_type_string()} = {self.default}"
        else:
            return f"{self.name}: {self.get_type_string()}"


@dataclass
class DateTimeProperty(Property):
    """ A property of type datetime.datetime """

    _type_string: ClassVar[str] = "datetime"

    def to_string(self) -> str:
        """ How this should be declared in a dataclass """
        return f"{self.name}: {self.get_type_string()}"


@dataclass
class FloatProperty(Property):
    """ A property of type float """

    default: Optional[float] = None
    _type_string: ClassVar[str] = "float"

    def to_string(self) -> str:
        """ How this should be declared in a dataclass """
        if self.default:
            return f"{self.name}: {self.get_type_string()} = {self.default}"
        else:
            return f"{self.name}: {self.get_type_string()}"


@dataclass
class IntProperty(Property):
    """ A property of type int """

    default: Optional[int] = None
    _type_string: ClassVar[str] = "int"

    def to_string(self) -> str:
        """ How this should be declared in a dataclass """
        if self.default:
            return f"{self.name}: {self.get_type_string()} = {self.default}"
        else:
            return f"{self.name}: {self.get_type_string()}"


@dataclass
class BooleanProperty(Property):
    """ Property for bool """

    _type_string: ClassVar[str] = "bool"

    def to_string(self) -> str:
        """ How this should be declared in a dataclass """
        return f"{self.name}: {self.get_type_string()}"


@dataclass
class ListProperty(Property):
    """ Property for list """

    type: Optional[str]
    ref: Optional[str]

    def get_type_string(self):
        """ Get a string representation of type that should be used when declaring this property """
        if self.required:
            return f"List[{self.type}]"
        return f"Optional[List[{self.type}]]"

    def to_string(self) -> str:
        """ How this should be declared in a dataclass """
        return f"{self.name}: {self.get_type_string()}"


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

    def to_string(self) -> str:
        """ How this should be declared in a dataclass """
        return f"{self.name}: {self.get_type_string()}"

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

    ref: str

    def get_type_string(self):
        """ Get a string representation of type that should be used when declaring this property """
        if self.required:
            return self.ref
        return f"Optional[{self.ref}]"

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
        return EnumProperty(name=name, required=required, values=EnumProperty.values_from_list(data["enum"]))
    if "$ref" in data:
        ref = data["$ref"].split("/")[-1]
        return RefProperty(name=name, required=required, ref=ref)
    if data["type"] == "string":
        if "format" not in data:
            return StringProperty(
                name=name, default=data.get("default"), required=required, pattern=data.get("pattern"),
            )
        elif data["format"] == "date-time":
            return DateTimeProperty(name=name, required=required)
    elif data["type"] == "number":
        return FloatProperty(name=name, default=data.get("default"), required=required)
    elif data["type"] == "integer":
        return IntProperty(name=name, default=data.get("default"), required=required)
    elif data["type"] == "boolean":
        return BooleanProperty(name=name, required=required)
    elif data["type"] == "array":
        ref = None
        if "$ref" in data["items"]:
            ref = data["items"]["$ref"].split("/")[-1]
        _type = None
        if "type" in data["items"]:
            _type = _openapi_types_to_python_type_strings[data["items"]["type"]]
        return ListProperty(name=name, required=required, type=_type, ref=ref)
    elif data["type"] == "object":
        return DictProperty(name=name, required=required)
    raise ValueError(f"Did not recognize type of {data}")
