from dataclasses import dataclass
from typing import Optional, List, Dict, Union


@dataclass
class Property:
    """ Describes a single property for a schema """

    name: str
    required: bool


@dataclass
class StringProperty(Property):
    """ A property of type str """

    max_length: Optional[int] = None
    default: Optional[str] = None
    pattern: Optional[str] = None


@dataclass
class DateTimeProperty(Property):
    """ A property of type datetime.datetime """

    pass


@dataclass
class FloatProperty(Property):
    """ A property of type float """

    default: Optional[float] = None


@dataclass
class IntProperty(Property):
    """ A property of type int """

    default: Optional[int] = None


@dataclass
class BooleanProperty(Property):
    """ Property for bool """

    pass


@dataclass
class ListProperty(Property):
    """ Property for list """

    type: Optional[str] = None
    ref: Optional[str] = None


@dataclass
class EnumProperty(Property):
    """ A property that should use an enum """

    values: List[str]


@dataclass
class RefProperty(Property):
    """ A property which refers to another Schema """

    ref: str


@dataclass
class DictProperty(Property):
    """ Property that is a general Dict """


def property_from_dict(
    name: str, required: bool, data: Dict[str, Union[float, int, str, List[str], Dict[str, str]]]
) -> Property:
    if "enum" in data:
        return EnumProperty(name=name, required=required, values=data["enum"],)
    if "$ref" in data:
        ref = data["$ref"].split("/")[-1]
        return RefProperty(name=name, required=required, ref=ref,)
    if data["type"] == "string":
        if "format" not in data:
            return StringProperty(
                name=name, default=data.get("default"), required=required, pattern=data.get("pattern"),
            )
        elif data["format"] == "date-time":
            return DateTimeProperty(name=name, required=required,)
    elif data["type"] == "number":
        return FloatProperty(name=name, default=data.get("default"), required=required,)
    elif data["type"] == "integer":
        return IntProperty(name=name, default=data.get("default"), required=required,)
    elif data["type"] == "boolean":
        return BooleanProperty(name=name, required=required,)
    elif data["type"] == "array":
        ref = None
        if "$ref" in data["items"]:
            ref = data["items"]["$ref"].split("/")[-1]
        return ListProperty(name=name, required=required, type=data["items"].get("type"), ref=ref,)
    elif data["type"] == "object":
        return DictProperty(name=name, required=required,)
    raise ValueError(f"Did not recognize type of {data}")
