from typing import List, Set, Tuple, Union, Optional

import attr

from ... import Config
from ... import schema as oai
from ... import utils
from ..errors import ParseError, PropertyError, ValidationError
from .converter import convert
from .enum_property import EnumProperty
from .model_property import build_model_property
from .property import Property
from .schemas import ReferencePath, Schemas, parse_reference_path
from .enum_property import get_enum_default, build_enum_property
from .union_property import build_union_property
from .types import (
    AnyProperty,
    StringProperty,
    DateTimeProperty,
    DateProperty,
    FileProperty,
    BooleanProperty,
    FloatProperty,
    IntProperty,
)
from .list_property import build_list_property


# pylint: disable=too-many-arguments
def _property_from_ref(
    name: str,
    required: bool,
    parent: Union[oai.Schema, None],
    data: oai.Reference,
    schemas: Schemas,
    config: Config,
    roots: Set[Union[ReferencePath, utils.ClassName]],
) -> Tuple[Union[Property, PropertyError], Schemas]:
    ref_path = parse_reference_path(data.ref)
    if isinstance(ref_path, ParseError):
        return PropertyError(data=data, detail=ref_path.detail), schemas
    existing = schemas.classes_by_reference.get(ref_path)
    if not existing:
        return PropertyError(data=data, detail="Could not find reference in parsed models or enums"), schemas

    prop = attr.evolve(
        existing,
        required=required,
        name=name,
        python_name=utils.PythonIdentifier(value=name, prefix=config.field_prefix),
    )
    if parent:
        prop = attr.evolve(prop, nullable=parent.nullable)
        if isinstance(prop, EnumProperty):
            default = get_enum_default(prop, parent)
            if isinstance(default, PropertyError):
                return default, schemas
            prop = attr.evolve(prop, default=default)

    schemas.add_dependencies(ref_path=ref_path, roots=roots)
    return prop, schemas


# pylint: disable=too-many-arguments,too-many-return-statements
def _property_from_data(
    name: str,
    required: bool,
    data: Union[oai.Reference, oai.Schema],
    schemas: Schemas,
    parent_name: str,
    config: Config,
    process_properties: bool,
    roots: Set[Union[ReferencePath, utils.ClassName]],
) -> Tuple[Union[Property, PropertyError], Schemas]:
    """Generate a Property from the OpenAPI dictionary representation of it"""
    name = utils.remove_string_escapes(name)
    if isinstance(data, oai.Reference):
        return _property_from_ref(
            name=name, required=required, parent=None, data=data, schemas=schemas, config=config, roots=roots
        )

    sub_data: List[Union[oai.Schema, oai.Reference]] = data.allOf + data.anyOf + data.oneOf
    # A union of a single reference should just be passed through to that reference (don't create copy class)
    if len(sub_data) == 1 and isinstance(sub_data[0], oai.Reference):
        return _property_from_ref(
            name=name, required=required, parent=data, data=sub_data[0], schemas=schemas, config=config, roots=roots
        )

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
    if data.anyOf or data.oneOf:
        return build_union_property(
            data=data, name=name, required=required, schemas=schemas, parent_name=parent_name, config=config
        )
    if data.type == oai.DataType.STRING:
        return _string_based_property(name=name, required=required, data=data, config=config), schemas
    if data.type == oai.DataType.NUMBER:
        return (
            FloatProperty(
                name=name,
                default=convert("float", data.default),
                required=required,
                nullable=data.nullable,
                python_name=utils.PythonIdentifier(value=name, prefix=config.field_prefix),
                description=data.description,
                example=data.example,
            ),
            schemas,
        )
    if data.type == oai.DataType.INTEGER:
        return (
            IntProperty(
                name=name,
                default=convert("int", data.default),
                required=required,
                nullable=data.nullable,
                python_name=utils.PythonIdentifier(value=name, prefix=config.field_prefix),
                description=data.description,
                example=data.example,
            ),
            schemas,
        )
    if data.type == oai.DataType.BOOLEAN:
        return (
            BooleanProperty(
                name=name,
                required=required,
                default=convert("bool", data.default),
                nullable=data.nullable,
                python_name=utils.PythonIdentifier(value=name, prefix=config.field_prefix),
                description=data.description,
                example=data.example,
            ),
            schemas,
        )
    if data.type == oai.DataType.ARRAY:
        return build_list_property(
            data=data,
            name=name,
            required=required,
            schemas=schemas,
            parent_name=parent_name,
            config=config,
            process_properties=process_properties,
            roots=roots,
        )
    if data.type == oai.DataType.OBJECT or data.allOf or (data.type is None and data.properties):
        return build_model_property(
            data=data,
            name=name,
            schemas=schemas,
            required=required,
            parent_name=parent_name,
            config=config,
            process_properties=process_properties,
            roots=roots,
        )
    return (
        AnyProperty(
            name=name,
            required=required,
            nullable=False,
            default=None,
            python_name=utils.PythonIdentifier(value=name, prefix=config.field_prefix),
            description=data.description,
            example=data.example,
        ),
        schemas,
    )


def _string_based_property(
    name: str, required: bool, data: oai.Schema, config: Config
) -> Union[StringProperty, DateProperty, DateTimeProperty, FileProperty]:
    """Construct a Property from the type "string" """
    string_format = data.schema_format
    python_name = utils.PythonIdentifier(value=name, prefix=config.field_prefix)
    if string_format == "date-time":
        return DateTimeProperty(
            name=name,
            required=required,
            default=convert("datetime.datetime", data.default),
            nullable=data.nullable,
            python_name=python_name,
            description=data.description,
            example=data.example,
        )
    if string_format == "date":
        return DateProperty(
            name=name,
            required=required,
            default=convert("datetime.date", data.default),
            nullable=data.nullable,
            python_name=python_name,
            description=data.description,
            example=data.example,
        )
    if string_format == "binary":
        return FileProperty(
            name=name,
            required=required,
            default=None,
            nullable=data.nullable,
            python_name=python_name,
            description=data.description,
            example=data.example,
        )
    return StringProperty(
        name=name,
        default=convert("str", data.default),
        required=required,
        pattern=data.pattern,
        nullable=data.nullable,
        python_name=python_name,
        description=data.description,
        example=data.example,
    )


def property_from_data(
    *,
    name: str,
    required: bool,
    data: Union[oai.Reference, oai.Schema],
    schemas: Schemas,
    parent_name: str,
    config: Config,
    process_properties: bool = True,
    roots: Optional[Set[Union[ReferencePath, utils.ClassName]]] = None,
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
        process_properties: If the new property is a ModelProperty, determines whether it will be initialized with
            property data
        roots: The set of `ReferencePath`s and `ClassName`s to remove from the schemas if a child reference becomes
            invalid
    Returns:
        A tuple containing either the parsed Property or a PropertyError (if something went wrong) and the updated
        Schemas (including any new classes that should be generated).
    """
    roots = roots or set()
    try:
        return _property_from_data(
            name=name,
            required=required,
            data=data,
            schemas=schemas,
            parent_name=parent_name,
            config=config,
            process_properties=process_properties,
            roots=roots,
        )
    except ValidationError:
        return PropertyError(detail="Failed to validate default value", data=data), schemas
