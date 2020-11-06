from itertools import chain
from typing import Any, ClassVar, Dict, Generic, List, Optional, Set, Tuple, TypeVar, Union

import attr

from ... import schema as oai
from ... import utils
from ..errors import PropertyError, ValidationError
from ..reference import Reference
from .converter import convert, convert_chain
from .enum_property import EnumProperty
from .model_property import ModelProperty
from .property import Property
from .schemas import Schemas


@attr.s(auto_attribs=True, frozen=True, slots=True)
class StringProperty(Property):
    """ A property of type str """

    max_length: Optional[int] = None
    pattern: Optional[str] = None
    _type_string: ClassVar[str] = "str"


@attr.s(auto_attribs=True, frozen=True, slots=True)
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


@attr.s(auto_attribs=True, frozen=True, slots=True)
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


@attr.s(auto_attribs=True, frozen=True, slots=True)
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


@attr.s(auto_attribs=True, frozen=True, slots=True)
class FloatProperty(Property):
    """ A property of type float """

    _type_string: ClassVar[str] = "float"


@attr.s(auto_attribs=True, frozen=True, slots=True)
class IntProperty(Property):
    """ A property of type int """

    _type_string: ClassVar[str] = "int"


@attr.s(auto_attribs=True, frozen=True, slots=True)
class BooleanProperty(Property):
    """ Property for bool """

    _type_string: ClassVar[str] = "bool"


InnerProp = TypeVar("InnerProp", bound=Property)


@attr.s(auto_attribs=True, frozen=True, slots=True)
class ListProperty(Property, Generic[InnerProp]):
    """ A property representing a list (array) of other properties """

    inner_property: InnerProp
    template: ClassVar[str] = "list_property.pyi"

    def get_type_string(self, no_optional: bool = False) -> str:
        """ Get a string representation of type that should be used when declaring this property """
        type_string = f"List[{self.inner_property.get_type_string()}]"
        if no_optional:
            return type_string
        if self.nullable:
            type_string = f"Optional[{type_string}]"
        if not self.required:
            type_string = f"Union[Unset, {type_string}]"
        return type_string

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


@attr.s(auto_attribs=True, frozen=True, slots=True)
class UnionProperty(Property):
    """ A property representing a Union (anyOf) of other properties """

    inner_properties: List[Property]
    template: ClassVar[str] = "union_property.pyi"

    def get_type_string(self, no_optional: bool = False) -> str:
        """ Get a string representation of type that should be used when declaring this property """
        inner_types = [p.get_type_string(no_optional=True) for p in self.inner_properties]
        inner_prop_string = ", ".join(inner_types)
        type_string = f"Union[{inner_prop_string}]"
        if no_optional:
            return type_string
        if not self.required:
            type_string = f"Union[Unset, {inner_prop_string}]"
        if self.nullable:
            type_string = f"Optional[{type_string}]"
        return type_string

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


def _string_based_property(
    name: str, required: bool, data: oai.Schema
) -> Union[StringProperty, DateProperty, DateTimeProperty, FileProperty]:
    """ Construct a Property from the type "string" """
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


def build_model_property(
    *, data: oai.Schema, name: str, schemas: Schemas, required: bool
) -> Tuple[Union[ModelProperty, PropertyError], Schemas]:
    """
    A single ModelProperty from its OAI data

    Args:
        data: Data of a single Schema
        name: Name by which the schema is referenced, such as a model name.
            Used to infer the type name if a `title` property is not available.
        schemas: Existing Schemas which have already been processed (to check name conflicts)
    """
    required_set = set(data.required or [])
    required_properties: List[Property] = []
    optional_properties: List[Property] = []
    relative_imports: Set[str] = set()

    ref = Reference.from_ref(data.title or name)

    for key, value in (data.properties or {}).items():
        required = key in required_set
        prop, schemas = property_from_data(name=key, required=required, data=value, schemas=schemas)
        if isinstance(prop, PropertyError):
            return prop, schemas
        if required and not prop.nullable:
            required_properties.append(prop)
        else:
            optional_properties.append(prop)
        relative_imports.update(prop.get_imports(prefix=".."))

    prop = ModelProperty(
        reference=ref,
        required_properties=required_properties,
        optional_properties=optional_properties,
        relative_imports=relative_imports,
        description=data.description or "",
        default=None,
        nullable=data.nullable,
        required=required,
        name=name,
    )
    schemas = attr.evolve(schemas, models={**schemas.models, prop.reference.class_name: prop})
    return prop, schemas


def build_enum_property(
    *, data: oai.Schema, name: str, required: bool, schemas: Schemas, enum: List[Union[str, int]]
) -> Tuple[Union[EnumProperty, PropertyError], Schemas]:

    reference = Reference.from_ref(data.title or name)
    values = EnumProperty.values_from_list(enum)

    dedup_counter = 0  # TODO: use the parent names instead of a counter for deduping
    while reference.class_name in schemas.enums:
        existing = schemas.enums[reference.class_name]
        if values == existing.values:
            break  # This is the same Enum, we're good
        dedup_counter += 1
        reference = Reference.from_ref(f"{reference.class_name}{dedup_counter}")

    for value in values.values():
        value_type = type(value)
        break
    else:
        return PropertyError(data=data, detail="No values provided for Enum"), schemas

    default = None
    if data.default is not None:
        inverse_values = {v: k for k, v in values.items()}
        try:
            default = f"{reference.class_name}.{inverse_values[data.default]}"
        except KeyError:
            return (
                PropertyError(
                    detail=f"{data.default} is an invalid default for enum {reference.class_name}", data=data
                ),
                schemas,
            )

    prop = EnumProperty(
        name=name,
        required=required,
        default=default,
        nullable=data.nullable,
        reference=reference,
        values=values,
        value_type=value_type,
    )
    schemas = attr.evolve(schemas, enums={**schemas.enums, prop.reference.class_name: prop})
    return prop, schemas


def build_union_property(
    *, data: oai.Schema, name: str, required: bool, schemas: Schemas
) -> Tuple[Union[UnionProperty, PropertyError], Schemas]:
    sub_properties: List[Property] = []
    for sub_prop_data in chain(data.anyOf, data.oneOf):
        sub_prop, schemas = property_from_data(name=name, required=required, data=sub_prop_data, schemas=schemas)
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
    *, data: oai.Schema, name: str, required: bool, schemas: Schemas
) -> Tuple[Union[ListProperty[Any], PropertyError], Schemas]:
    if data.items is None:
        return PropertyError(data=data, detail="type array must have items defined"), schemas
    inner_prop, schemas = property_from_data(name=f"{name}_item", required=True, data=data.items, schemas=schemas)
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


def _property_from_data(
    name: str,
    required: bool,
    data: Union[oai.Reference, oai.Schema],
    schemas: Schemas,
) -> Tuple[Union[Property, PropertyError], Schemas]:
    """ Generate a Property from the OpenAPI dictionary representation of it """
    name = utils.remove_string_escapes(name)
    if isinstance(data, oai.Reference):
        reference = Reference.from_ref(data.ref)
        existing = schemas.enums.get(reference.class_name) or schemas.models.get(reference.class_name)
        if existing:
            return (
                attr.evolve(existing, required=required, name=name),
                schemas,
            )
        return PropertyError(data=data, detail="Could not find reference in parsed models or enums"), schemas
    if data.enum:
        return build_enum_property(data=data, name=name, required=required, schemas=schemas, enum=data.enum)
    if data.anyOf or data.oneOf:
        return build_union_property(data=data, name=name, required=required, schemas=schemas)
    if not data.type:
        return PropertyError(data=data, detail="Schemas must either have one of enum, anyOf, or type defined."), schemas

    if data.type == "string":
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
        return build_list_property(data=data, name=name, required=required, schemas=schemas)
    elif data.type == "object":
        return build_model_property(data=data, name=name, schemas=schemas, required=required)
    return PropertyError(data=data, detail=f"unknown type {data.type}"), schemas


def property_from_data(
    name: str,
    required: bool,
    data: Union[oai.Reference, oai.Schema],
    schemas: Schemas,
) -> Tuple[Union[Property, PropertyError], Schemas]:
    try:
        return _property_from_data(name=name, required=required, data=data, schemas=schemas)
    except ValidationError:
        return PropertyError(detail="Failed to validate default value", data=data), schemas


def update_schemas_with_data(name: str, data: oai.Schema, schemas: Schemas) -> Union[Schemas, PropertyError]:
    if data.enum is not None:
        prop, schemas = build_enum_property(data=data, name=name, required=True, schemas=schemas, enum=data.enum)
    else:
        prop, schemas = build_model_property(data=data, name=name, schemas=schemas, required=True)
    if isinstance(prop, PropertyError):
        return prop
    else:
        return schemas


def build_schemas(*, components: Dict[str, Union[oai.Reference, oai.Schema]]) -> Schemas:
    """ Get a list of Schemas from an OpenAPI dict """
    schemas = Schemas()
    to_process = components.items()
    processing = True
    errors = []

    # References could have forward References so keep going as long as we are making progress
    while processing:
        processing = False
        errors = []
        next_round = []
        # Only accumulate errors from the last round, since we might fix some along the way
        for name, data in to_process:
            if isinstance(data, oai.Reference):
                schemas.errors.append(PropertyError(data=data, detail="Reference schemas are not supported."))
                continue
            schemas_or_err = update_schemas_with_data(name, data, schemas)
            if isinstance(schemas_or_err, PropertyError):
                next_round.append((name, data))
                errors.append(schemas_or_err)
            else:
                schemas = schemas_or_err
                processing = True  # We made some progress this round, do another after it's done
        to_process = next_round
    schemas.errors.extend(errors)

    return schemas
