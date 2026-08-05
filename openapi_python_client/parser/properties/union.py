from __future__ import annotations

from collections.abc import Iterator
from itertools import chain
from typing import Any, ClassVar, cast

from attr import define, evolve, field

from ... import Config
from ... import schema as oai
from ...utils import PythonIdentifier
from ..errors import ParseError, PropertyError
from .protocol import PropertyProtocol, Value
from .schemas import Schemas, parse_reference_path


def _registered_member(
    sub_prop_data: oai.Schema | oai.Reference,
    sub_prop: PropertyProtocol,
    schemas: Schemas,
) -> PropertyProtocol:
    """The property object registered in `schemas` for a union member, falling back to the member itself.

    For a `$ref`, `property_from_data` hands back a per-use copy which is snapshotted before the referenced
    schema's own properties have been processed, so the copy's `required_properties` stays `None` forever. The
    registered object is the one that gets filled in later, in place.
    """
    if not isinstance(sub_prop_data, oai.Reference):
        # An inline schema is only built once, so the property we just built *is* the registered one.
        return sub_prop
    ref_path = parse_reference_path(sub_prop_data.ref)
    if isinstance(ref_path, ParseError):  # pragma: no cover -- property_from_data already resolved this ref
        return sub_prop
    return schemas.classes_by_reference.get(ref_path, sub_prop)


@define
class UnionProperty(PropertyProtocol):
    """A property representing a Union (anyOf) of other properties"""

    name: str
    required: bool
    default: Value | None
    python_name: PythonIdentifier
    description: str | None
    example: str | None
    inner_properties: list[PropertyProtocol]
    discriminator_property_name: str | None = None
    """`propertyName` of the OpenAPI `discriminator`, if this union or one flattened into it declared one."""
    registered_members: dict[str, PropertyProtocol] = field(factory=dict)
    """Members by type string, as the objects registered in `Schemas` rather than the copies in
    `inner_properties`. See `_registered_member`; `get_discriminator_field_name` needs the processed versions."""
    template: ClassVar[str] = "union_property.py.jinja"

    @classmethod
    def build(
        cls,
        *,
        data: oai.Schema,
        name: str,
        required: bool,
        schemas: Schemas,
        parent_name: str,
        config: Config,
    ) -> tuple[UnionProperty | PropertyError, Schemas]:
        """
        Create a `UnionProperty` the right way.

        Args:
            data: The `Schema` describing the `UnionProperty`.
            name: The name of the property where it appears in the OpenAPI document.
            required: Whether this property is required where it's being used.
            schemas: The `Schemas` so far describing existing classes / references.
            parent_name: The name of the thing which holds this property (used for renaming inner classes).
            config: User-defined config values for modifying inner properties.

        Returns:
            `(result, schemas)` where `schemas` is the updated version of the input `schemas` and `result` is the
                constructed `UnionProperty` or a `PropertyError` describing what went wrong.
        """
        from . import property_from_data  # noqa: PLC0415

        sub_properties: list[PropertyProtocol] = []
        registered_members: dict[str, PropertyProtocol] = {}
        discriminator_names: set[str] = set()
        own_discriminator = data.discriminator.propertyName if data.discriminator is not None else None
        if own_discriminator:
            discriminator_names.add(own_discriminator)

        type_list_data = []
        if isinstance(data.type, list):
            for _type in data.type:
                type_list_data.append(data.model_copy(update={"type": _type, "default": None}))

        for i, sub_prop_data in enumerate(chain(data.anyOf, data.oneOf, type_list_data)):
            # If a schema has a unique title property, we can use that to carry forward a descriptive name instead of "type_0"
            subscript: str
            if (
                isinstance(sub_prop_data, oai.Schema)
                and sub_prop_data.title is not None
                and sub_prop_data.title != data.title
            ):
                subscript = sub_prop_data.title
            else:
                subscript = f"type_{i}"

            sub_prop, schemas = property_from_data(
                name=f"{name}_{subscript}",
                required=True,
                data=sub_prop_data,
                schemas=schemas,
                parent_name=parent_name,
                config=config,
            )
            if isinstance(sub_prop, PropertyError):
                return (
                    PropertyError(detail=f"Invalid property in union {name}", data=sub_prop_data),
                    schemas,
                )
            sub_properties.append(sub_prop)
            if own_discriminator and not isinstance(sub_prop, UnionProperty):
                # Only unions that declare a discriminator have any use for these, and a nested union brings its
                # own along when it is flattened below.
                registered = _registered_member(sub_prop_data, sub_prop, schemas)
                registered_members[registered.get_base_type_string()] = registered

        def flatten_union_properties(possibly_nested: list[PropertyProtocol]) -> Iterator[PropertyProtocol]:
            for to_flatten in possibly_nested:
                if isinstance(to_flatten, UnionProperty):
                    # A nested union collapses into this one, so its discriminator and members come along with it.
                    # `Optional[Annotated[Union[...], Field(discriminator=...)]]` is written by pydantic itself as
                    # `anyOf: [{oneOf: [...], discriminator: ...}, {type: "null"}]`, which lands here.
                    if to_flatten.discriminator_property_name is not None:
                        discriminator_names.add(to_flatten.discriminator_property_name)
                    registered_members.update(to_flatten.registered_members)
                    yield from flatten_union_properties(to_flatten.inner_properties)
                else:
                    yield to_flatten

        seen_types = set()
        inner_properties: list[PropertyProtocol] = []
        for flattened in flatten_union_properties(sub_properties):
            type_string = flattened.get_type_string(no_optional=True)
            if type_string not in seen_types:
                seen_types.add(type_string)
                inner_properties.append(flattened)

        prop = UnionProperty(
            name=name,
            required=required,
            default=None,
            inner_properties=inner_properties,
            python_name=PythonIdentifier(value=name, prefix=config.field_prefix),
            description=data.description,
            example=data.example,
            # Members disagreeing about which property is the tag means there is no single tag to dispatch on.
            discriminator_property_name=discriminator_names.pop() if len(discriminator_names) == 1 else None,
            registered_members=registered_members,
        )
        default_or_error = prop.convert_value(data.default)
        if isinstance(default_or_error, PropertyError):
            default_or_error.data = data
            return default_or_error, schemas
        prop = evolve(prop, default=default_or_error)
        return prop, schemas

    def convert_value(self, value: Any) -> Value | None | PropertyError:
        if value is None or isinstance(value, Value):
            return None
        value_or_error: Value | PropertyError | None = PropertyError(
            detail=f"Invalid default value for union {self.name}"
        )
        for sub_prop in self.inner_properties:
            value_or_error = sub_prop.convert_value(value)
            if not isinstance(value_or_error, PropertyError):
                return value_or_error
        return value_or_error

    def _get_inner_type_strings(self, json: bool) -> set[str]:
        return {
            p.get_type_string(
                no_optional=True,
                json=json,
            )
            for p in self.inner_properties
        }

    @staticmethod
    def _get_type_string_from_inner_type_strings(inner_types: set[str]) -> str:
        if len(inner_types) == 1:
            return inner_types.pop()
        return " | ".join(sorted(inner_types, key=lambda x: x.lower()))

    def get_base_type_string(self) -> str:
        return self._get_type_string_from_inner_type_strings(self._get_inner_type_strings(json=False))

    def get_base_json_type_string(self) -> str:
        return self._get_type_string_from_inner_type_strings(self._get_inner_type_strings(json=True))

    def get_type_strings_in_union(self, *, no_optional: bool = False, json: bool) -> set[str]:
        """
        Get the set of all the types that should appear within the `Union` representing this property.

        This function is called from the union property macros, thus the public visibility.

        Args:
            no_optional: Do not include `None` or `Unset` in this set.
            json: If True, this returns the JSON types, not the Python types, of this property.

        Returns:
            A set of strings containing the types that should appear within `Union`.
        """
        type_strings = self._get_inner_type_strings(json=json)
        if no_optional:
            return type_strings
        if not self.required:
            type_strings.add("Unset")
        return type_strings

    def get_type_string(
        self,
        no_optional: bool = False,
        json: bool = False,
    ) -> str:
        """
        Get a string representation of type that should be used when declaring this property.
        This implementation differs slightly from `Property.get_type_string` in order to collapse
        nested union types.
        """
        type_strings_in_union = self.get_type_strings_in_union(no_optional=no_optional, json=json)
        return self._get_type_string_from_inner_type_strings(type_strings_in_union)

    def get_discriminator_field_name(self) -> str | None:
        """The field to hand pydantic's `Field(discriminator=...)`, or `None` to leave this union untagged.

        A tagged union accepts and serializes exactly what the untagged one does: pydantic tags each member by the
        `Literal` values of the member's own field, which is what the untagged union matches on anyway. So this only
        changes how pydantic dispatches -- more cheaply, and reporting the errors of the one member that was asked
        for instead of every member's.

        The catch is that pydantic rejects the whole *class* when its members cannot carry a tag, so everything
        pydantic requires has to hold before we ask for one. Each member must be a model whose tag field is
        required and annotated as a bare `Literal`, all of them must name that field identically (pydantic insists
        the alias be the same across members), and no value may claim two members. Anything else falls back to the
        plain union, which stays correct.

        This runs while rendering rather than while parsing because members are still being processed when unions
        are built -- see `registered_members`.
        """
        from .const import ConstProperty  # noqa: PLC0415
        from .literal_enum_property import LiteralEnumProperty  # noqa: PLC0415
        from .model_property import ModelProperty  # noqa: PLC0415
        from .none import NoneProperty  # noqa: PLC0415

        if self.discriminator_property_name is None:
            return None

        field_name: str | None = None
        tagged_count = 0
        seen_values: set[Any] = set()
        for inner_property in self.inner_properties:
            if isinstance(inner_property, NoneProperty):
                continue  # pydantic tolerates a null member alongside the tagged ones
            registered = self.registered_members.get(inner_property.get_base_type_string())
            if not isinstance(registered, ModelProperty) or registered.required_properties is None:
                return None
            tag = next(
                (prop for prop in registered.required_properties if prop.name == self.discriminator_property_name),
                None,
            )
            # Only these two render as a bare `Literal[...]`; an `EnumProperty` renders as an `Enum` subclass, and
            # an optional tag renders as `Literal[...] | None`, both of which pydantic refuses to tag on.
            if isinstance(tag, ConstProperty):
                values: set[Any] = {tag.value.raw_value}
            elif isinstance(tag, LiteralEnumProperty):
                values = set(tag.values)
            else:
                return None
            if (field_name is not None and field_name != tag.python_name) or values & seen_values:
                return None
            field_name = tag.python_name
            seen_values |= values
            tagged_count += 1

        return field_name if tagged_count > 1 else None

    def get_imports(self, *, prefix: str) -> set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names. This should be the number of . to get
            back to the root of the generated client.
        """
        imports = super().get_imports(prefix=prefix)
        for inner_prop in self.inner_properties:
            imports.update(inner_prop.get_imports(prefix=prefix))
        imports.add("from typing import cast")
        return imports

    def get_lazy_imports(self, *, prefix: str) -> set[str]:
        lazy_imports = super().get_lazy_imports(prefix=prefix)
        for inner_prop in self.inner_properties:
            lazy_imports.update(inner_prop.get_lazy_imports(prefix=prefix))
        return lazy_imports

    def validate_location(self, location: oai.ParameterLocation) -> ParseError | None:
        """Returns an error if this type of property is not allowed in the given location"""
        from ..properties import Property  # noqa: PLC0415

        for inner_prop in self.inner_properties:
            if evolve(cast(Property, inner_prop), required=self.required).validate_location(location) is not None:
                return ParseError(detail=f"{self.get_type_string()} is not allowed in {location}")
        return None
