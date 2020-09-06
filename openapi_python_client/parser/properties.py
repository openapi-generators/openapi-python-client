from dataclasses import InitVar, dataclass, field
from itertools import chain
from typing import Any, ClassVar, Dict, Generic, List, Optional, Set, Type, TypeVar, Union

from dateutil.parser import isoparse

from .. import schema as oai
from .. import utils
from .errors import PropertyError, ValidationError
from .reference import Reference


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
        self.python_name = utils.snake_case(self.name)
        if self.default is not None:
            self.default = self._validate_default(default=self.default)

    def _validate_default(self, default: Any) -> Any:
        """ Check that the default value is valid for the property's type + perform any necessary sanitization """
        raise ValidationError

    def get_type_string(self, no_optional: bool = False) -> str:
        """
        Get a string representation of type that should be used when declaring this property

        Args:
            no_optional: Do not include Optional even if the value is optional (needed for isinstance checks)
        """
        if no_optional or (self.required and not self.nullable):
            return self._type_string
        return f"Optional[{self._type_string}]"

    def get_imports(self, *, prefix: str) -> Set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names. This should be the number of . to get
            back to the root of the generated client.
        """
        if self.nullable or not self.required:
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


@dataclass
class StringProperty(Property):
    """ A property of type str """

    max_length: Optional[int] = None
    pattern: Optional[str] = None

    _type_string: ClassVar[str] = "str"

    def _validate_default(self, default: Any) -> str:
        return f"{utils.remove_string_escapes(default)!r}"


@dataclass
class DateTimeProperty(Property):
    """
    A property of type datetime.datetime
    """

    _type_string: ClassVar[str] = "datetime.datetime"
    template: ClassVar[str] = "datetime_property.pyi"

    def get_imports(self, *, prefix: str) -> Set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names. This should be the number of . to get
            back to the root of the generated client.
        """
        imports = super().get_imports(prefix=prefix)
        imports.update({"import datetime", "from typing import cast", "from dateutil.parser import isoparse"})
        return imports

    def _validate_default(self, default: Any) -> str:
        try:
            isoparse(default)
        except (TypeError, ValueError) as e:
            raise ValidationError from e
        return f"isoparse({default!r})"


@dataclass
class DateProperty(Property):
    """ A property of type datetime.date """

    _type_string: ClassVar[str] = "datetime.date"
    template: ClassVar[str] = "date_property.pyi"

    def get_imports(self, *, prefix: str) -> Set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names. This should be the number of . to get
            back to the root of the generated client.
        """
        imports = super().get_imports(prefix=prefix)
        imports.update({"import datetime", "from typing import cast", "from dateutil.parser import isoparse"})
        return imports

    def _validate_default(self, default: Any) -> str:
        try:
            isoparse(default).date()
        except (TypeError, ValueError) as e:
            raise ValidationError() from e
        return f"isoparse({default!r}).date()"


@dataclass
class FileProperty(Property):
    """ A property used for uploading files """

    _type_string: ClassVar[str] = "File"
    template: ClassVar[str] = "file_property.pyi"

    def get_imports(self, *, prefix: str) -> Set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names. This should be the number of . to get
            back to the root of the generated client.
        """
        imports = super().get_imports(prefix=prefix)
        imports.update({f"from {prefix}types import File"})
        return imports


@dataclass
class FloatProperty(Property):
    """ A property of type float """

    default: Optional[float] = None
    _type_string: ClassVar[str] = "float"

    def _validate_default(self, default: Any) -> float:
        try:
            return float(default)
        except (TypeError, ValueError) as e:
            raise ValidationError() from e


@dataclass
class IntProperty(Property):
    """ A property of type int """

    default: Optional[int] = None
    _type_string: ClassVar[str] = "int"

    def _validate_default(self, default: Any) -> int:
        try:
            return int(default)
        except (TypeError, ValueError) as e:
            raise ValidationError() from e


@dataclass
class BooleanProperty(Property):
    """ Property for bool """

    _type_string: ClassVar[str] = "bool"

    def _validate_default(self, default: Any) -> bool:
        # no try/except needed as anything that comes from the initial load from json/yaml will be boolable
        return bool(default)


InnerProp = TypeVar("InnerProp", bound=Property)


@dataclass
class ListProperty(Property, Generic[InnerProp]):
    """ A property representing a list (array) of other properties """

    inner_property: InnerProp
    template: ClassVar[str] = "list_property.pyi"

    def get_type_string(self, no_optional: bool = False) -> str:
        """ Get a string representation of type that should be used when declaring this property """
        if no_optional or (self.required and not self.nullable):
            return f"List[{self.inner_property.get_type_string()}]"
        return f"Optional[List[{self.inner_property.get_type_string()}]]"

    def get_imports(self, *, prefix: str) -> Set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names. This should be the number of . to get
            back to the root of the generated client.
        """
        imports = super().get_imports(prefix=prefix)
        imports.update(self.inner_property.get_imports(prefix=prefix))
        imports.add("from typing import List")
        return imports

    def _validate_default(self, default: Any) -> None:
        return None


@dataclass
class UnionProperty(Property):
    """ A property representing a Union (anyOf) of other properties """

    inner_properties: List[Property]
    template: ClassVar[str] = "union_property.pyi"

    def get_type_string(self, no_optional: bool = False) -> str:
        """ Get a string representation of type that should be used when declaring this property """
        inner_types = [p.get_type_string() for p in self.inner_properties]
        inner_prop_string = ", ".join(inner_types)
        if no_optional or (self.required and not self.nullable):
            return f"Union[{inner_prop_string}]"
        return f"Optional[Union[{inner_prop_string}]]"

    def get_imports(self, *, prefix: str) -> Set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names. This should be the number of . to get
            back to the root of the generated client.
        """
        imports = super().get_imports(prefix=prefix)
        for inner_prop in self.inner_properties:
            imports.update(inner_prop.get_imports(prefix=prefix))
        imports.add("from typing import Union")
        return imports

    def _validate_default(self, default: Any) -> Any:
        for property in self.inner_properties:
            try:
                val = property._validate_default(default)
                return val
            except ValidationError:
                continue
        raise ValidationError()


_existing_enums: Dict[str, "EnumProperty"] = {}
ValueType = Union[str, int]


@dataclass
class EnumProperty(Property):
    """ A property that should use an enum """

    values: Dict[str, ValueType]
    reference: Reference = field(init=False)
    title: InitVar[str]
    value_type: Type[ValueType] = field(init=False)

    template: ClassVar[str] = "enum_property.pyi"

    def __post_init__(self, title: str) -> None:  # type: ignore
        reference = Reference.from_ref(title)
        dedup_counter = 0
        while reference.class_name in _existing_enums:
            existing = _existing_enums[reference.class_name]
            if self.values == existing.values:
                break  # This is the same Enum, we're good
            dedup_counter += 1
            reference = Reference.from_ref(f"{reference.class_name}{dedup_counter}")

        self.reference = reference

        for value in self.values.values():
            self.value_type = type(value)
            break

        super().__post_init__()
        _existing_enums[self.reference.class_name] = self

    @staticmethod
    def get_all_enums() -> Dict[str, "EnumProperty"]:
        """ Get all the EnumProperties that have been registered keyed by class name """
        return _existing_enums

    @staticmethod
    def get_enum(name: str) -> Optional["EnumProperty"]:
        """ Get all the EnumProperties that have been registered keyed by class name """
        return _existing_enums.get(name)

    def get_type_string(self, no_optional: bool = False) -> str:
        """ Get a string representation of type that should be used when declaring this property """

        if no_optional or (self.required and not self.nullable):
            return self.reference.class_name
        return f"Optional[{self.reference.class_name}]"

    def get_imports(self, *, prefix: str) -> Set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names. This should be the number of . to get
            back to the root of the generated client.
        """
        imports = super().get_imports(prefix=prefix)
        imports.add(f"from {prefix}models.{self.reference.module_name} import {self.reference.class_name}")
        return imports

    @staticmethod
    def values_from_list(values: List[ValueType]) -> Dict[str, ValueType]:
        """ Convert a list of values into dict of {name: value} """
        output: Dict[str, ValueType] = {}

        for i, value in enumerate(values):
            if isinstance(value, int):
                output[f"VALUE_{value}"] = value
                continue
            if value[0].isalpha():
                key = value.upper()
            else:
                key = f"VALUE_{i}"
            if key in output:
                raise ValueError(f"Duplicate key {key} in Enum")
            sanitized_key = utils.fix_keywords(utils.sanitize(key))
            output[sanitized_key] = utils.remove_string_escapes(value)

        return output

    def _validate_default(self, default: Any) -> str:
        inverse_values = {v: k for k, v in self.values.items()}
        try:
            return f"{self.reference.class_name}.{inverse_values[default]}"
        except KeyError as e:
            raise ValidationError() from e


@dataclass
class RefProperty(Property):
    """ A property which refers to another Schema """

    reference: Reference

    @property
    def template(self) -> str:  # type: ignore
        enum = EnumProperty.get_enum(self.reference.class_name)
        if enum:
            return "enum_property.pyi"
        return "ref_property.pyi"

    def get_type_string(self, no_optional: bool = False) -> str:
        """ Get a string representation of type that should be used when declaring this property """
        if no_optional or (self.required and not self.nullable):
            return self.reference.class_name
        return f"Optional[{self.reference.class_name}]"

    def get_imports(self, *, prefix: str) -> Set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names. This should be the number of . to get
            back to the root of the generated client.
        """
        imports = super().get_imports(prefix=prefix)
        imports.update(
            {
                f"from {prefix}models.{self.reference.module_name} import {self.reference.class_name}",
                "from typing import Dict",
                "from typing import cast",
            }
        )
        return imports

    def _validate_default(self, default: Any) -> Any:
        enum = EnumProperty.get_enum(self.reference.class_name)
        if enum:
            return enum._validate_default(default)
        else:
            raise ValidationError


@dataclass
class DictProperty(Property):
    """ Property that is a general Dict """

    _type_string: ClassVar[str] = "Dict[Any, Any]"
    template: ClassVar[str] = "dict_property.pyi"

    def get_imports(self, *, prefix: str) -> Set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names. This should be the number of . to get
            back to the root of the generated client.
        """
        imports = super().get_imports(prefix=prefix)
        imports.add("from typing import Dict")
        if self.default is not None:
            imports.add("from dataclasses import field")
            imports.add("from typing import cast")
        return imports

    def _validate_default(self, default: Any) -> None:
        return None


def _string_based_property(
    name: str, required: bool, data: oai.Schema
) -> Union[StringProperty, DateProperty, DateTimeProperty, FileProperty]:
    """ Construct a Property from the type "string" """
    string_format = data.schema_format
    if string_format == "date-time":
        return DateTimeProperty(
            name=name,
            required=required,
            default=data.default,
            nullable=data.nullable,
        )
    elif string_format == "date":
        return DateProperty(
            name=name,
            required=required,
            default=data.default,
            nullable=data.nullable,
        )
    elif string_format == "binary":
        return FileProperty(
            name=name,
            required=required,
            default=data.default,
            nullable=data.nullable,
        )
    else:
        return StringProperty(
            name=name,
            default=data.default,
            required=required,
            pattern=data.pattern,
            nullable=data.nullable,
        )


def _property_from_data(
    name: str, required: bool, data: Union[oai.Reference, oai.Schema]
) -> Union[Property, PropertyError]:
    """ Generate a Property from the OpenAPI dictionary representation of it """
    name = utils.remove_string_escapes(name)
    if isinstance(data, oai.Reference):
        return RefProperty(
            name=name,
            required=required,
            reference=Reference.from_ref(data.ref),
            default=None,
            nullable=False,
        )
    if data.enum:
        return EnumProperty(
            name=name,
            required=required,
            values=EnumProperty.values_from_list(data.enum),
            title=data.title or name,
            default=data.default,
            nullable=data.nullable,
        )
    if data.anyOf or data.oneOf:
        sub_properties: List[Property] = []
        for sub_prop_data in chain(data.anyOf, data.oneOf):
            sub_prop = property_from_data(name=name, required=required, data=sub_prop_data)
            if isinstance(sub_prop, PropertyError):
                return PropertyError(detail=f"Invalid property in union {name}", data=sub_prop_data)
            sub_properties.append(sub_prop)
        return UnionProperty(
            name=name,
            required=required,
            default=data.default,
            inner_properties=sub_properties,
            nullable=data.nullable,
        )
    if not data.type:
        return PropertyError(data=data, detail="Schemas must either have one of enum, anyOf, or type defined.")
    if data.type == "string":
        return _string_based_property(name=name, required=required, data=data)
    elif data.type == "number":
        return FloatProperty(
            name=name,
            default=data.default,
            required=required,
            nullable=data.nullable,
        )
    elif data.type == "integer":
        return IntProperty(
            name=name,
            default=data.default,
            required=required,
            nullable=data.nullable,
        )
    elif data.type == "boolean":
        return BooleanProperty(
            name=name,
            required=required,
            default=data.default,
            nullable=data.nullable,
        )
    elif data.type == "array":
        if data.items is None:
            return PropertyError(data=data, detail="type array must have items defined")
        inner_prop = property_from_data(name=f"{name}_item", required=True, data=data.items)
        if isinstance(inner_prop, PropertyError):
            return PropertyError(data=inner_prop.data, detail=f"invalid data in items of array {name}")
        return ListProperty(
            name=name,
            required=required,
            default=data.default,
            inner_property=inner_prop,
            nullable=data.nullable,
        )
    elif data.type == "object":
        return DictProperty(
            name=name,
            required=required,
            default=data.default,
            nullable=data.nullable,
        )
    return PropertyError(data=data, detail=f"unknown type {data.type}")


def property_from_data(
    name: str, required: bool, data: Union[oai.Reference, oai.Schema]
) -> Union[Property, PropertyError]:
    try:
        return _property_from_data(name=name, required=required, data=data)
    except ValidationError:
        return PropertyError(detail="Failed to validate default value", data=data)
