from dataclasses import dataclass, replace
from itertools import chain
from typing import Any, ClassVar, Dict, Generic, List, Optional, Set, Tuple, TypeVar, Union

from dateutil.parser import isoparse

from ... import schema as oai
from ... import utils
from ..errors import PropertyError, ValidationError
from ..reference import Reference
from .enum_property import EnumProperty
from .model_property import ModelProperty
from .property import Property
from .schemas import Schemas


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
        if required:
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
    schemas = replace(schemas, models={**schemas.models, prop.reference.class_name: prop})
    return prop, schemas


def build_enum_property(
    *, data: oai.Schema, name: str, required: bool, schemas: Schemas, enum: List[Union[str, int]]
) -> Tuple[EnumProperty, Schemas]:
    prop = EnumProperty(
        name=name,
        required=required,
        values=EnumProperty.values_from_list(enum),
        title=data.title or name,
        default=data.default,
        nullable=data.nullable,
        existing_enums=schemas.enums,
    )
    schemas = replace(schemas, enums={**schemas.enums, prop.reference.class_name: prop})
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
    return (
        UnionProperty(
            name=name,
            required=required,
            default=data.default,
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
            default=data.default,
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
        if reference.class_name in schemas.enums:
            return schemas.enums[reference.class_name], schemas
        elif reference.class_name in schemas.models:
            return schemas.models[reference.class_name], schemas
        else:
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
                default=data.default,
                required=required,
                nullable=data.nullable,
            ),
            schemas,
        )
    elif data.type == "integer":
        return (
            IntProperty(
                name=name,
                default=data.default,
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
                default=data.default,
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


def build_schemas(*, components: Dict[str, Union[oai.Reference, oai.Schema]]) -> Schemas:
    """ Get a list of Schemas from an OpenAPI dict """
    schemas = Schemas()
    for name, data in components.items():
        if isinstance(data, oai.Reference):
            schemas.errors.append(PropertyError(data=data, detail="Reference schemas are not supported."))
            continue
        if data.enum is not None:
            prop, schemas = build_enum_property(data=data, name=name, required=True, schemas=schemas, enum=data.enum)
            continue
        model, schemas = build_model_property(data=data, name=name, schemas=schemas, required=True)
        if isinstance(model, PropertyError):
            schemas.errors.append(model)
    return schemas
