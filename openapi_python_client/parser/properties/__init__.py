import copy
from itertools import chain
from typing import Any, ClassVar, Dict, Generic, Iterable, Iterator, List, Optional, Set, Tuple, TypeVar, Union, cast

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


class LazyReferencePropertyProxy:

    __GLOBAL_SCHEMAS_REF: Schemas = Schemas()
    __PROXIES: List[Tuple["LazyReferencePropertyProxy", oai.Reference]] = []

    @classmethod
    def update_schemas(cls, schemas: Schemas) -> None:
        cls.__GLOBAL_SCHEMAS_REF = schemas

    @classmethod
    def create(cls, name: str, required: bool, data: oai.Reference, parent_name: str) -> "LazyReferencePropertyProxy":
        proxy = LazyReferencePropertyProxy(name, required, data, parent_name)
        cls.__PROXIES.append((proxy, data))
        return proxy

    @classmethod
    def created_proxies(cls) -> List[Tuple["LazyReferencePropertyProxy", oai.Reference]]:
        return cls.__PROXIES

    @classmethod
    def flush_internal_references(cls) -> None:
        cls.__PROXIES = []
        cls.__GLOBAL_SCHEMAS_REF = Schemas()

    def __init__(self, name: str, required: bool, data: oai.Reference, parent_name: str):
        self._name = name
        self._required = required
        self._data = data
        self._parent_name = parent_name
        self._reference: Reference = Reference.from_ref(data.ref)
        self._reference_to_itself: bool = self._reference.class_name == parent_name
        self._resolved: Union[Property, None] = None

    def get_instance_type_string(self) -> str:
        return self.get_type_string(no_optional=True)

    def get_type_string(self, no_optional: bool = False) -> str:
        resolved = self.resolve()
        if resolved:
            return resolved.get_type_string(no_optional)
        return "LazyReferencePropertyProxy"

    def get_imports(self, *, prefix: str) -> Set[str]:
        resolved = self.resolve()
        if resolved:
            return resolved.get_imports(prefix=prefix)
        return set()

    def __copy__(self) -> Property:
        resolved = cast(Property, self.resolve(False))
        return copy.copy(resolved)

    def __deepcopy__(self, memo: Any) -> Property:
        resolved = cast(Property, self.resolve(False))
        return copy.deepcopy(resolved, memo)

    def __getattr__(self, name: str) -> Any:
        resolved = self.resolve(False)
        return resolved.__getattribute__(name)

    def resolve(self, allow_lazyness: bool = True) -> Union[Property, None]:
        if not self._resolved:
            schemas = LazyReferencePropertyProxy.__GLOBAL_SCHEMAS_REF
            class_name = self._reference.class_name
            if schemas:
                existing = schemas.enums.get(class_name) or schemas.models.get(class_name)
                if existing:
                    self._resolved = attr.evolve(existing, required=self._required, name=self._name)

        if self._resolved:
            return self._resolved
        elif allow_lazyness:
            return None
        else:
            raise RuntimeError(f"Reference {self._data} shall have been resolved.")


@attr.s(auto_attribs=True, frozen=True)
class NoneProperty(Property):
    """ A property that is always None (used for empty schemas) """

    _type_string: ClassVar[str] = "None"
    template: ClassVar[Optional[str]] = "none_property.py.jinja"


@attr.s(auto_attribs=True, frozen=True)
class StringProperty(Property):
    """ A property of type str """

    max_length: Optional[int] = None
    pattern: Optional[str] = None
    _type_string: ClassVar[str] = "str"


@attr.s(auto_attribs=True, frozen=True)
class DateTimeProperty(Property):
    """
    A property of type datetime.datetime
    """

    _type_string: ClassVar[str] = "datetime.datetime"
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
    """ A property of type datetime.date """

    _type_string: ClassVar[str] = "datetime.date"
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
    """ A property used for uploading files """

    _type_string: ClassVar[str] = "File"
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
    """ A property of type float """

    _type_string: ClassVar[str] = "float"


@attr.s(auto_attribs=True, frozen=True)
class IntProperty(Property):
    """ A property of type int """

    _type_string: ClassVar[str] = "int"


@attr.s(auto_attribs=True, frozen=True)
class BooleanProperty(Property):
    """ Property for bool """

    _type_string: ClassVar[str] = "bool"


InnerProp = TypeVar("InnerProp", bound=Property)


@attr.s(auto_attribs=True, frozen=True)
class ListProperty(Property, Generic[InnerProp]):
    """ A property representing a list (array) of other properties """

    inner_property: InnerProp
    template: ClassVar[str] = "list_property.py.jinja"

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
    """ A property representing a Union (anyOf) of other properties """

    inner_properties: List[Property]
    template: ClassVar[str] = "union_property.py.jinja"
    has_properties_without_templates: bool = attr.ib(init=False)

    def __attrs_post_init__(self) -> None:
        super().__attrs_post_init__()
        object.__setattr__(
            self, "has_properties_without_templates", any(prop.template is None for prop in self.inner_properties)
        )

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
        imports.add("from typing import cast, Union")
        return imports

    def inner_properties_with_template(self) -> Iterator[Property]:
        return (prop for prop in self.inner_properties if prop.template)


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
    *, data: oai.Schema, name: str, schemas: Schemas, required: bool, parent_name: Optional[str]
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

    class_name = data.title or name
    if parent_name:
        class_name = f"{utils.pascal_case(parent_name)}{utils.pascal_case(class_name)}"
    ref = Reference.from_ref(class_name)

    for key, value in (data.properties or {}).items():
        prop_required = key in required_set
        prop, schemas = property_from_data(
            name=key, required=prop_required, data=value, schemas=schemas, parent_name=class_name
        )
        if isinstance(prop, PropertyError):
            return prop, schemas
        if prop_required and not prop.nullable:
            required_properties.append(prop)
        else:
            optional_properties.append(prop)
        relative_imports.update(prop.get_imports(prefix=".."))

    additional_properties: Union[bool, Property, PropertyError]
    if data.additionalProperties is None:
        additional_properties = True
    elif isinstance(data.additionalProperties, bool):
        additional_properties = data.additionalProperties
    elif isinstance(data.additionalProperties, oai.Schema) and not any(data.additionalProperties.dict().values()):
        # An empty schema
        additional_properties = True
    else:
        assert isinstance(data.additionalProperties, (oai.Schema, oai.Reference))
        additional_properties, schemas = property_from_data(
            name="AdditionalProperty",
            required=True,  # in the sense that if present in the dict will not be None
            data=data.additionalProperties,
            schemas=schemas,
            parent_name=class_name,
        )
        if isinstance(additional_properties, PropertyError):
            return additional_properties, schemas
        relative_imports.update(additional_properties.get_imports(prefix=".."))

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
        additional_properties=additional_properties,
    )
    if prop.reference.class_name in schemas.models:
        error = PropertyError(
            data=data, detail=f'Attempted to generate duplicate models with name "{prop.reference.class_name}"'
        )
        return error, schemas

    schemas = attr.evolve(schemas, models={**schemas.models, prop.reference.class_name: prop})
    return prop, schemas


def build_enum_property(
    *,
    data: oai.Schema,
    name: str,
    required: bool,
    schemas: Schemas,
    enum: List[Union[str, int]],
    parent_name: Optional[str],
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

    Returns:
        A tuple containing either the created property or a PropertyError describing what went wrong AND update schemas.
    """

    class_name = data.title or name
    if parent_name:
        class_name = f"{utils.pascal_case(parent_name)}{utils.pascal_case(class_name)}"
    reference = Reference.from_ref(class_name)
    values = EnumProperty.values_from_list(enum)

    if reference.class_name in schemas.enums:
        existing = schemas.enums[reference.class_name]
        if values != existing.values:
            return (
                PropertyError(
                    detail=f"Found conflicting enums named {reference.class_name} with incompatible values.", data=data
                ),
                schemas,
            )

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
    *, data: oai.Schema, name: str, required: bool, schemas: Schemas, parent_name: str
) -> Tuple[Union[UnionProperty, PropertyError], Schemas]:
    sub_properties: List[Property] = []
    for sub_prop_data in chain(data.anyOf, data.oneOf):
        sub_prop, schemas = property_from_data(
            name=name, required=required, data=sub_prop_data, schemas=schemas, parent_name=parent_name
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
    *, data: oai.Schema, name: str, required: bool, schemas: Schemas, parent_name: str
) -> Tuple[Union[ListProperty[Any], PropertyError], Schemas]:
    if data.items is None:
        return PropertyError(data=data, detail="type array must have items defined"), schemas
    inner_prop, schemas = property_from_data(
        name=f"{name}_item", required=True, data=data.items, schemas=schemas, parent_name=parent_name
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


def _property_from_data(
    name: str,
    required: bool,
    data: Union[oai.Reference, oai.Schema],
    schemas: Schemas,
    parent_name: str,
) -> Tuple[Union[Property, PropertyError], Schemas]:
    """ Generate a Property from the OpenAPI dictionary representation of it """
    name = utils.remove_string_escapes(name)
    if isinstance(data, oai.Reference):
        if not _is_local_reference(data):
            return PropertyError(data=data, detail="Remote reference schemas are not supported."), schemas

        reference = Reference.from_ref(data.ref)
        existing = schemas.enums.get(reference.class_name) or schemas.models.get(reference.class_name)
        if existing:
            return (
                attr.evolve(existing, required=required, name=name),
                schemas,
            )
        else:
            return cast(Property, LazyReferencePropertyProxy.create(name, required, data, parent_name)), schemas

    if data.enum:
        return build_enum_property(
            data=data, name=name, required=required, schemas=schemas, enum=data.enum, parent_name=parent_name
        )
    if data.anyOf or data.oneOf:
        return build_union_property(data=data, name=name, required=required, schemas=schemas, parent_name=parent_name)
    if not data.type:
        return NoneProperty(name=name, required=required, nullable=False, default=None), schemas

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
        return build_list_property(data=data, name=name, required=required, schemas=schemas, parent_name=parent_name)
    elif data.type == "object":
        return build_model_property(data=data, name=name, schemas=schemas, required=required, parent_name=parent_name)
    return PropertyError(data=data, detail=f"unknown type {data.type}"), schemas


def property_from_data(
    *,
    name: str,
    required: bool,
    data: Union[oai.Reference, oai.Schema],
    schemas: Schemas,
    parent_name: str,
) -> Tuple[Union[Property, PropertyError], Schemas]:
    try:
        return _property_from_data(name=name, required=required, data=data, schemas=schemas, parent_name=parent_name)
    except ValidationError:
        return PropertyError(detail="Failed to validate default value", data=data), schemas


def update_schemas_with_data(name: str, data: oai.Schema, schemas: Schemas) -> Union[Schemas, PropertyError]:
    prop: Union[PropertyError, ModelProperty, EnumProperty]
    if data.enum is not None:
        prop, schemas = build_enum_property(
            data=data, name=name, required=True, schemas=schemas, enum=data.enum, parent_name=None
        )
    else:
        prop, schemas = build_model_property(data=data, name=name, schemas=schemas, required=True, parent_name=None)

    if isinstance(prop, PropertyError):
        return prop
    else:
        return schemas


def resolve_reference_and_update_schemas(
    name: str, data: oai.Reference, schemas: Schemas, references_by_name: Dict[str, oai.Reference]
) -> Union[Schemas, PropertyError]:
    if _is_local_reference(data):
        return _resolve_local_reference_schema(name, data, schemas, references_by_name)
    else:
        return _resolve_remote_reference_schema(name, data, schemas, references_by_name)


def _resolve_local_reference_schema(
    name: str, data: oai.Reference, schemas: Schemas, references_by_name: Dict[str, oai.Reference]
) -> Union[Schemas, PropertyError]:
    resolved_model_or_enum = _resolve_model_or_enum_reference(name, data, schemas, references_by_name)

    if resolved_model_or_enum:
        model_name = utils.pascal_case(name)

        if isinstance(resolved_model_or_enum, EnumProperty):
            schemas.enums[model_name] = resolved_model_or_enum

        elif isinstance(resolved_model_or_enum, ModelProperty):
            schemas.models[model_name] = resolved_model_or_enum

        return schemas
    else:
        return PropertyError(data=data, detail="Failed to resolve local reference schemas.")


def _resolve_model_or_enum_reference(
    name: str, data: oai.Reference, schemas: Schemas, references_by_name: Dict[str, oai.Reference]
) -> Union[EnumProperty, ModelProperty, None]:
    target_model = _reference_model_name(data)
    target_name = _reference_name(data)

    if target_model == name or target_name == name:
        return None  # Avoid infinite loop

    if target_name in references_by_name:
        return _resolve_model_or_enum_reference(
            target_name, references_by_name[target_name], schemas, references_by_name
        )

    if target_model in schemas.enums:
        return schemas.enums[target_model]
    elif target_model in schemas.models:
        return schemas.models[target_model]

    return None


def _resolve_remote_reference_schema(
    name: str, data: oai.Reference, schemas: Schemas, references_by_name: Dict[str, oai.Reference]
) -> Union[Schemas, PropertyError]:
    return PropertyError(data=data, detail="Remote reference schemas are not supported.")


def _is_local_reference(reference: oai.Reference) -> bool:
    return reference.ref.startswith("#", 0)


def _reference_model_name(reference: oai.Reference) -> str:
    return Reference.from_ref(reference.ref).class_name


def _reference_name(reference: oai.Reference) -> str:
    parts = reference.ref.split("/")
    return parts[-1]


def build_schemas(*, components: Dict[str, Union[oai.Reference, oai.Schema]]) -> Schemas:
    """ Get a list of Schemas from an OpenAPI dict """
    schemas = Schemas()
    to_process: Iterable[Tuple[str, Union[oai.Reference, oai.Schema]]] = components.items()
    processing = True
    errors: List[PropertyError] = []
    references_by_name: Dict[str, oai.Reference] = dict()
    references_to_process: List[Tuple[str, oai.Reference]] = list()
    LazyReferencePropertyProxy.flush_internal_references()  # Cleanup side effects

    # References could have forward References so keep going as long as we are making progress
    while processing:
        processing = False
        errors = []
        next_round = []
        # Only accumulate errors from the last round, since we might fix some along the way
        for name, data in to_process:
            if isinstance(data, oai.Reference):
                references_by_name[name] = data
                references_to_process.append((name, data))
                continue

            schemas_or_err = update_schemas_with_data(name, data, schemas)

            if isinstance(schemas_or_err, PropertyError):
                next_round.append((name, data))
                errors.append(schemas_or_err)
            else:
                schemas = schemas_or_err
                processing = True  # We made some progress this round, do another after it's donea

        to_process = next_round

    for name, reference in references_to_process:
        schemas_or_err = resolve_reference_and_update_schemas(name, reference, schemas, references_by_name)

        if isinstance(schemas_or_err, PropertyError):
            errors.append(schemas_or_err)

    schemas.errors.extend(errors)
    LazyReferencePropertyProxy.update_schemas(schemas)
    for reference_proxy, data in LazyReferencePropertyProxy.created_proxies():
        if not reference_proxy.resolve():
            schemas.errors.append(
                PropertyError(data=data, detail="Could not find reference in parsed models or enums.")
            )
    return schemas
