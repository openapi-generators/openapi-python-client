from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, List, Optional

from .reference import Reference


@dataclass
class Property:
    """ Describes a single property for a schema """

    name: str
    required: bool
    default: Optional[Any]

    constructor_template: ClassVar[Optional[str]] = None
    _type_string: ClassVar[str]

    def get_type_string(self) -> str:
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

    def transform(self) -> str:
        """ What it takes to turn this object into a native python type """
        return self.name

    def constructor_from_dict(self, dict_name: str) -> str:
        """ How to load this property from a dict (used in generated model from_dict function """
        if self.required:
            return f'{dict_name}["{self.name}"]'
        else:
            return f'{dict_name}.get("{self.name}")'


@dataclass
class StringProperty(Property):
    """ A property of type str """

    max_length: Optional[int] = None
    pattern: Optional[str] = None

    _type_string: ClassVar[str] = "str"

    def __post_init__(self) -> None:
        if self.default is not None:
            self.default = f'"{self.default}"'


@dataclass
class DateTimeProperty(Property):
    """ A property of type datetime.datetime """

    _type_string: ClassVar[str] = "datetime"
    constructor_template: ClassVar[str] = "datetime_property.pyi"


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
class BasicListProperty(Property):
    """ A List of basic types """

    type: str

    def constructor_from_dict(self, dict_name: str) -> str:
        """ How to set this property from a dictionary of values """
        return f'{dict_name}.get("{self.name}", [])'

    def get_type_string(self) -> str:
        """ Get a string representation of type that should be used when declaring this property """
        if self.required:
            return f"List[{self.type}]"
        return f"Optional[List[{self.type}]]"


@dataclass
class ReferenceListProperty(Property):
    """ A List of References """

    reference: Reference
    constructor_template: ClassVar[str] = "reference_list_property.pyi"

    def get_type_string(self) -> str:
        """ Get a string representation of type that should be used when declaring this property """
        if self.required:
            return f"List[{self.reference.class_name}]"
        return f"Optional[List[{self.reference.class_name}]]"


@dataclass
class EnumListProperty(Property):
    """ List of Enum values """

    values: Dict[str, str]
    reference: Reference = field(init=False)
    constructor_template: ClassVar[str] = "enum_list_property.pyi"

    def __post_init__(self) -> None:
        self.reference = Reference.from_ref(self.name)

    def get_type_string(self) -> str:
        """ Get a string representation of type that should be used when declaring this property """
        if self.required:
            return f"List[{self.reference.class_name}]"
        return f"Optional[List[{self.reference.class_name}]]"


@dataclass
class EnumProperty(Property):
    """ A property that should use an enum """

    values: Dict[str, str]
    reference: Reference = field(init=False)

    def __post_init__(self) -> None:
        self.reference = Reference.from_ref(self.name)
        inverse_values = {v: k for k, v in self.values.items()}
        if self.default is not None:
            self.default = f"{self.reference.class_name}.{inverse_values[self.default]}"

    def get_type_string(self) -> str:
        """ Get a string representation of type that should be used when declaring this property """

        if self.required:
            return self.reference.class_name
        return f"Optional[{self.reference.class_name}]"

    def transform(self) -> str:
        """ Output to the template, convert this Enum into a JSONable value """
        return f"{self.name}.value"

    def constructor_from_dict(self, dict_name: str) -> str:
        """ How to load this property from a dict (used in generated model from_dict function """
        return f'{self.reference.class_name}({dict_name}["{self.name}"]) if "{self.name}" in {dict_name} else None'

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

    def transform(self) -> str:
        """ Convert this into a JSONable value """
        return f"{self.name}.to_dict()"


@dataclass
class DictProperty(Property):
    """ Property that is a general Dict """

    _type_string: ClassVar[str] = "Dict"


_openapi_types_to_python_type_strings = {
    "string": "str",
    "number": "float",
    "integer": "int",
    "boolean": "bool",
    "object": "Dict",
}


def property_from_dict(name: str, required: bool, data: Dict[str, Any]) -> Property:
    """ Generate a Property from the OpenAPI dictionary representation of it """
    if "enum" in data:
        return EnumProperty(
            name=name,
            required=required,
            values=EnumProperty.values_from_list(data["enum"]),
            default=data.get("default"),
        )
    if "$ref" in data:
        return RefProperty(name=name, required=required, reference=Reference.from_ref(data["$ref"]), default=None)
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
        if "$ref" in data["items"]:
            return ReferenceListProperty(
                name=name, required=required, default=None, reference=Reference.from_ref(data["items"]["$ref"])
            )
        if "enum" in data["items"]:
            return EnumListProperty(
                name=name, required=required, default=None, values=EnumProperty.values_from_list(data["items"]["enum"])
            )
        if "type" in data["items"]:
            return BasicListProperty(
                name=name,
                required=required,
                default=None,
                type=_openapi_types_to_python_type_strings[data["items"]["type"]],
            )
    elif data["type"] == "object":
        return DictProperty(name=name, required=required, default=data.get("default"))
    raise ValueError(f"Did not recognize type of {data}")
