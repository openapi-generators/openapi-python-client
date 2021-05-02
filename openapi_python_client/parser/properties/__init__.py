__all__ = [
    "Class",
    "EnumProperty",
    "ModelProperty",
    "NoneProperty",
    "Property",
    "Schemas",
    "build_schemas",
    "property_from_data",
]

from itertools import chain
from typing import Any, ClassVar, Dict, Generic, Iterable, Iterator, List, Optional, Set, Tuple, TypeVar, Union

import attr

from ... import Config
from ... import schema as oai
from ... import utils
from ..errors import ParseError, PropertyError, ValidationError
from .converter import convert, convert_chain
from .enum_property import EnumProperty
from .model_property import ModelProperty, build_model_property
from .property import Property
from .schemas import Class, Schemas, parse_reference_path, update_schemas_with_data


@attr.s(auto_attribs=True, frozen=True)
class NoneProperty(Property):
    """A property that is always None (used for empty schemas)"""

    _type_string: ClassVar[str] = "None"
    _json_type_string: ClassVar[str] = "None"
    template: ClassVar[Optional[str]] = "none_property.py.jinja"


@attr.s(auto_attribs=True, frozen=True)
class StringProperty(Property):
    """A property of type str"""

    max_length: Optional[int] = None
    pattern: Optional[str] = None
    _type_string: ClassVar[str] = "str"
    _json_type_string: ClassVar[str] = "str"


@attr.s(auto_attribs=True, frozen=True)
class DateTimeProperty(Property):
    """
    A property of type datetime.datetime
    """

    _type_string: ClassVar[str] = "datetime.datetime"
    _json_type_string: ClassVar[str] = "str"
    template: ClassVar[str] = "datetime_property.py.jinja"

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


@attr.s(auto_attribs=True, frozen=True)
class DateProperty(Property):
    """A property of type datetime.date"""

    _type_string: ClassVar[str] = "datetime.date"
    _json_type_string: ClassVar[str] = "str"
    template: ClassVar[str] = "date_property.py.jinja"

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


@attr.s(auto_attribs=True, frozen=True)
class FileProperty(Property):
    """A property used for uploading files"""

    _type_string: ClassVar[str] = "File"
    # Return type of File.to_tuple()
    _json_type_string: ClassVar[str] = "Tuple[Optional[str], Union[BinaryIO, TextIO], Optional[str]]"
    template: ClassVar[str] = "file_property.py.jinja"

    def get_imports(self, *, prefix: str) -> Set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names. This should be the number of . to get
            back to the root of the generated client.
        """
        imports = super().get_imports(prefix=prefix)
        imports.update({f"from {prefix}types import File", "from io import BytesIO"})
        return imports


@attr.s(auto_attribs=True, frozen=True)
class FloatProperty(Property):
    """A property of type float"""

    _type_string: ClassVar[str] = "float"
    _json_type_string: ClassVar[str] = "float"


@attr.s(auto_attribs=True, frozen=True)
class IntProperty(Property):
    """A property of type int"""

    _type_string: ClassVar[str] = "int"
    _json_type_string: ClassVar[str] = "int"


@attr.s(auto_attribs=True, frozen=True)
class BooleanProperty(Property):
    """Property for bool"""

    _type_string: ClassVar[str] = "bool"
    _json_type_string: ClassVar[str] = "bool"


InnerProp = TypeVar("InnerProp", bound=Property)


@attr.s(auto_attribs=True, frozen=True)
class ListProperty(Property, Generic[InnerProp]):
    """A property representing a list (array) of other properties"""

    inner_property: InnerProp
    template: ClassVar[str] = "list_property.py.jinja"

    def get_base_type_string(self) -> str:
        return f"List[{self.inner_property.get_type_string()}]"

    def get_base_json_type_string(self) -> str:
        return f"List[{self.inner_property.get_type_string(json=True)}]"

    def get_instance_type_string(self) -> str:
        """Get a string representation of runtime type that should be used for `isinstance` checks"""
        return "list"

    def get_imports(self, *, prefix: str) -> Set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names. This should be the number of . to get
            back to the root of the generated client.
        """
        imports = super().get_imports(prefix=prefix)
        imports.update(self.inner_property.get_imports(prefix=prefix))
        imports.add("from typing import cast, List")
        return imports


@attr.s(auto_attribs=True, frozen=True)
class UnionProperty(Property):
    """A property representing a Union (anyOf) of other properties"""

    inner_properties: List[Property]
    template: ClassVar[str] = "union_property.py.jinja"
    has_properties_without_templates: bool = attr.ib(init=False)

    def __attrs_post_init__(self) -> None:
        super().__attrs_post_init__()
        object.__setattr__(
            self, "has_properties_without_templates", any(prop.template is None for prop in self.inner_properties)
        )

    def _get_inner_type_strings(self, json: bool = False) -> Set[str]:
        return {p.get_type_string(no_optional=True, json=json) for p in self.inner_properties}

    def _get_type_string_from_inner_type_strings(self, inner_types: Set[str]) -> str:
        if len(inner_types) == 1:
            return inner_types.pop()
        else:
            return f"Union[{', '.join(sorted(inner_types))}]"

    def get_base_type_string(self) -> str:
        return self._get_type_string_from_inner_type_strings(self._get_inner_type_strings(json=False))

    def get_base_json_type_string(self) -> str:
        return self._get_type_string_from_inner_type_strings(self._get_inner_type_strings(json=True))

    def get_type_strings_in_union(self, no_optional: bool = False, json: bool = False) -> Set[str]:
        type_strings = self._get_inner_type_strings(json=json)
        if no_optional:
            return type_strings
        if self.nullable:
            type_strings.add("None")
        if not self.required:
            type_strings.add("Unset")
        return type_strings

    def get_type_string(self, no_optional: bool = False, json: bool = False) -> str:
        """
        Get a string representation of type that should be used when declaring this property.
        This implementation differs slightly from `Property.get_type_string` in order to collapse
        nested union types.
        """
        type_strings_in_union = self.get_type_strings_in_union(no_optional=no_optional, json=json)
        return self._get_type_string_from_inner_type_strings(type_strings_in_union)

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
        imports.add("from typing import cast, Union")
        return imports

    def inner_properties_with_template(self) -> Iterator[Property]:
        return (prop for prop in self.inner_properties if prop.template)


def _string_based_property(
    name: str, required: bool, data: oai.Schema
) -> Union[StringProperty, DateProperty, DateTimeProperty, FileProperty]:
    """Construct a Property from the type "string" """
    string_format = data.schema_format
    if string_format == "date-time":
        return DateTimeProperty(
            name=name,
            required=required,
            default=convert("datetime.datetime", data.default),
            nullable=data.nullable,
        )
    elif string_format == "date":
        return DateProperty(
            name=name,
            required=required,
            default=convert("datetime.date", data.default),
            nullable=data.nullable,
        )
    elif string_format == "binary":
        return FileProperty(
            name=name,
            required=required,
            default=None,
            nullable=data.nullable,
        )
    else:
        return StringProperty(
            name=name,
            default=convert("str", data.default),
            required=required,
            pattern=data.pattern,
            nullable=data.nullable,
        )


def build_enum_property(
    *,
    data: oai.Schema,
    name: str,
    required: bool,
    schemas: Schemas,
    enum: List[Union[str, int]],
    parent_name: Optional[str],
    config: Config,
) -> Tuple[Union[EnumProperty, PropertyError], Schemas]:
    """
    Create an EnumProperty from schema data.

    Args:
        data: The OpenAPI Schema which defines this enum.
        name: The name to use for variables which receive this Enum's value (e.g. model property name)
        required: Whether or not this Property is required in the calling context
        schemas: The Schemas which have been defined so far (used to prevent naming collisions)
        enum: The enum from the provided data. Required separately here to prevent extra type checking.
        parent_name: The context in which this EnumProperty is defined, used to create more specific class names.
        config: The global config for this run of the generator

    Returns:
        A tuple containing either the created property or a PropertyError describing what went wrong AND update schemas.
    """

    class_name = data.title or name
    if parent_name:
        class_name = f"{utils.pascal_case(parent_name)}{utils.pascal_case(class_name)}"
    class_info = Class.from_string(string=class_name, config=config)
    values = EnumProperty.values_from_list(enum)

    if class_info.name in schemas.classes_by_name:
        existing = schemas.classes_by_name[class_info.name]
        if not isinstance(existing, EnumProperty) or values != existing.values:
            return (
                PropertyError(
                    detail=f"Found conflicting enums named {class_info.name} with incompatible values.", data=data
                ),
                schemas,
            )

    for value in values.values():
        value_type = type(value)
        break
    else:
        return PropertyError(data=data, detail="No values provided for Enum"), schemas

    prop = EnumProperty(
        name=name,
        required=required,
        nullable=data.nullable,
        class_info=class_info,
        values=values,
        value_type=value_type,
        default=None,
    )

    default = get_enum_default(prop, data)
    if isinstance(default, PropertyError):
        return default, schemas
    prop = attr.evolve(prop, default=default)

    schemas = attr.evolve(schemas, classes_by_name={**schemas.classes_by_name, class_info.name: prop})
    return prop, schemas


def get_enum_default(prop: EnumProperty, data: oai.Schema) -> Union[Optional[Any], PropertyError]:
    if data.default is None:
        return None

    inverse_values = {v: k for k, v in prop.values.items()}
    try:
        return f"{prop.class_info.name}.{inverse_values[data.default]}"
    except KeyError:
        return PropertyError(detail=f"{data.default} is an invalid default for enum {prop.class_info.name}", data=data)


def build_union_property(
    *, data: oai.Schema, name: str, required: bool, schemas: Schemas, parent_name: str, config: Config
) -> Tuple[Union[UnionProperty, PropertyError], Schemas]:
    sub_properties: List[Property] = []
    for i, sub_prop_data in enumerate(chain(data.anyOf, data.oneOf)):
        sub_prop, schemas = property_from_data(
            name=f"{name}_type{i}",
            required=required,
            data=sub_prop_data,
            schemas=schemas,
            parent_name=parent_name,
            config=config,
        )
        if isinstance(sub_prop, PropertyError):
            return PropertyError(detail=f"Invalid property in union {name}", data=sub_prop_data), schemas
        sub_properties.append(sub_prop)

    default = convert_chain((prop._type_string for prop in sub_properties), data.default)
    return (
        UnionProperty(
            name=name,
            required=required,
            default=default,
            inner_properties=sub_properties,
            nullable=data.nullable,
        ),
        schemas,
    )


def build_list_property(
    *, data: oai.Schema, name: str, required: bool, schemas: Schemas, parent_name: str, config: Config
) -> Tuple[Union[ListProperty[Any], PropertyError], Schemas]:
    if data.items is None:
        return PropertyError(data=data, detail="type array must have items defined"), schemas
    inner_prop, schemas = property_from_data(
        name=f"{name}_item", required=True, data=data.items, schemas=schemas, parent_name=parent_name, config=config
    )
    if isinstance(inner_prop, PropertyError):
        return PropertyError(data=inner_prop.data, detail=f"invalid data in items of array {name}"), schemas
    return (
        ListProperty(
            name=name,
            required=required,
            default=None,
            inner_property=inner_prop,
            nullable=data.nullable,
        ),
        schemas,
    )


def _property_from_ref(
    name: str,
    required: bool,
    parent: Union[oai.Schema, None],
    data: oai.Reference,
    schemas: Schemas,
) -> Tuple[Union[Property, PropertyError], Schemas]:
    ref_path = parse_reference_path(data.ref)
    if isinstance(ref_path, ParseError):
        return PropertyError(data=data, detail=ref_path.detail), schemas
    existing = schemas.classes_by_reference.get(ref_path)
    if not existing:
        return PropertyError(data=data, detail="Could not find reference in parsed models or enums"), schemas

    prop = attr.evolve(existing, required=required, name=name)
    if parent:
        prop = attr.evolve(prop, nullable=parent.nullable)
        if isinstance(prop, EnumProperty):
            default = get_enum_default(prop, parent)
            if isinstance(default, PropertyError):
                return default, schemas
            prop = attr.evolve(prop, default=default)

    return prop, schemas


def _property_from_data(
    name: str,
    required: bool,
    data: Union[oai.Reference, oai.Schema],
    schemas: Schemas,
    parent_name: str,
    config: Config,
) -> Tuple[Union[Property, PropertyError], Schemas]:
    """Generate a Property from the OpenAPI dictionary representation of it"""
    name = utils.remove_string_escapes(name)
    if isinstance(data, oai.Reference):
        return _property_from_ref(name=name, required=required, parent=None, data=data, schemas=schemas)

    # A union of a single reference should just be passed through to that reference (don't create copy class)
    sub_data = (data.allOf or []) + data.anyOf + data.oneOf
    if len(sub_data) == 1 and isinstance(sub_data[0], oai.Reference):
        return _property_from_ref(name=name, required=required, parent=data, data=sub_data[0], schemas=schemas)

    if data.enum:
        return build_enum_property(
            data=data,
            name=name,
            required=required,
            schemas=schemas,
            enum=data.enum,
            parent_name=parent_name,
            config=config,
        )
    elif data.anyOf or data.oneOf:
        return build_union_property(
            data=data, name=name, required=required, schemas=schemas, parent_name=parent_name, config=config
        )
    elif data.type == "string":
        return _string_based_property(name=name, required=required, data=data), schemas
    elif data.type == "number":
        return (
            FloatProperty(
                name=name,
                default=convert("float", data.default),
                required=required,
                nullable=data.nullable,
            ),
            schemas,
        )
    elif data.type == "integer":
        return (
            IntProperty(
                name=name,
                default=convert("int", data.default),
                required=required,
                nullable=data.nullable,
            ),
            schemas,
        )
    elif data.type == "boolean":
        return (
            BooleanProperty(
                name=name,
                required=required,
                default=convert("bool", data.default),
                nullable=data.nullable,
            ),
            schemas,
        )
    elif data.type == "array":
        return build_list_property(
            data=data, name=name, required=required, schemas=schemas, parent_name=parent_name, config=config
        )
    elif data.type == "object" or data.allOf:
        return build_model_property(
            data=data, name=name, schemas=schemas, required=required, parent_name=parent_name, config=config
        )
    elif not data.type:
        return NoneProperty(name=name, required=required, nullable=False, default=None), schemas
    return PropertyError(data=data, detail=f"unknown type {data.type}"), schemas


def property_from_data(
    *,
    name: str,
    required: bool,
    data: Union[oai.Reference, oai.Schema],
    schemas: Schemas,
    parent_name: str,
    config: Config,
) -> Tuple[Union[Property, PropertyError], Schemas]:
    """
    Build a Property from an OpenAPI schema or reference. This Property represents a single input or output for a
    generated API operation.

    Args:
        name: The name of the property, defined in OpenAPI as the key pointing at the schema. This is the parameter used
            to send this data to an API or that the API will respond with. This will be used to generate a `python_name`
            which is the name of the variable/attribute in generated Python.
        required: Whether or not this property is required in whatever source is creating it. OpenAPI defines this by
            including the property's name in the `required` list. If the property is required, `Unset` will not be
            included in the generated code's available types.
        data: The OpenAPI schema or reference that defines the details of this property (e.g. type, sub-properties).
        schemas: A structure containing all of the parsed schemas so far that will become generated classes. This is
            used to resolve references and to ensure that conflicting class names are not generated.
        parent_name: The name of the thing above this property, prepended to generated class names to reduce the chance
            of duplication.
        config: Contains the parsed config that the user provided to tweak generation settings. Needed to apply class
            name overrides for generated classes.

    Returns:
        A tuple containing either the parsed Property or a PropertyError (if something went wrong) and the updated
        Schemas (including any new classes that should be generated).
    """
    try:
        return _property_from_data(
            name=name, required=required, data=data, schemas=schemas, parent_name=parent_name, config=config
        )
    except ValidationError:
        return PropertyError(detail="Failed to validate default value", data=data), schemas


def build_schemas(
    *, components: Dict[str, Union[oai.Reference, oai.Schema]], schemas: Schemas, config: Config
) -> Schemas:
    """Get a list of Schemas from an OpenAPI dict"""
    to_process: Iterable[Tuple[str, Union[oai.Reference, oai.Schema]]] = components.items()
    still_making_progress = True
    errors: List[PropertyError] = []

    # References could have forward References so keep going as long as we are making progress
    while still_making_progress:
        still_making_progress = False
        errors = []
        next_round = []
        # Only accumulate errors from the last round, since we might fix some along the way
        for name, data in to_process:
            if isinstance(data, oai.Reference):
                schemas.errors.append(PropertyError(data=data, detail="Reference schemas are not supported."))
                continue
            ref_path = parse_reference_path(f"#/components/schemas/{name}")
            if isinstance(ref_path, ParseError):
                schemas.errors.append(PropertyError(detail=ref_path.detail, data=data))
                continue
            schemas_or_err = update_schemas_with_data(ref_path=ref_path, data=data, schemas=schemas, config=config)
            if isinstance(schemas_or_err, PropertyError):
                next_round.append((name, data))
                errors.append(schemas_or_err)
                continue
            schemas = schemas_or_err
            still_making_progress = True
        to_process = next_round

    schemas.errors.extend(errors)
    return schemas
