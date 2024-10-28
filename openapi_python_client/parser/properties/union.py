from __future__ import annotations

from itertools import chain
from typing import Any, ClassVar, cast

from attr import define, evolve

from ... import Config
from ... import schema as oai
from ...utils import PythonIdentifier
from ..errors import ParseError, PropertyError
from .protocol import PropertyProtocol, Value
from .schemas import Schemas, get_reference_simple_name, parse_reference_path


@define
class DiscriminatorDefinition:
    property_name: str
    value_to_model_map: dict[str, PropertyProtocol]
    # Every value in the map is really a ModelProperty, but this avoids circular imports


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
    discriminators: list[DiscriminatorDefinition] | None = None
    template: ClassVar[str] = "union_property.py.jinja"

    @classmethod
    def build(
        cls, *, data: oai.Schema, name: str, required: bool, schemas: Schemas, parent_name: str, config: Config
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
        from . import property_from_data

        sub_properties: list[PropertyProtocol] = []

        type_list_data = []
        if isinstance(data.type, list):
            for _type in data.type:
                type_list_data.append(data.model_copy(update={"type": _type, "default": None}))

        for i, sub_prop_data in enumerate(chain(data.anyOf, data.oneOf, type_list_data)):
            sub_prop, schemas = property_from_data(
                name=f"{name}_type_{i}",
                required=True,
                data=sub_prop_data,
                schemas=schemas,
                parent_name=parent_name,
                config=config,
            )
            if isinstance(sub_prop, PropertyError):
                return PropertyError(detail=f"Invalid property in union {name}", data=sub_prop_data), schemas
            sub_properties.append(sub_prop)

        sub_properties, discriminators_list = _flatten_union_properties(sub_properties)

        prop = UnionProperty(
            name=name,
            required=required,
            default=None,
            inner_properties=sub_properties,
            python_name=PythonIdentifier(value=name, prefix=config.field_prefix),
            description=data.description,
            example=data.example,
        )
        default_or_error = prop.convert_value(data.default)
        if isinstance(default_or_error, PropertyError):
            default_or_error.data = data
            return default_or_error, schemas
        prop = evolve(prop, default=default_or_error)

        if data.discriminator:
            discriminator_or_error = _parse_discriminator(data.discriminator, sub_properties, schemas)
            if isinstance(discriminator_or_error, PropertyError):
                return discriminator_or_error, schemas
            discriminators_list = [discriminator_or_error, *discriminators_list]
        if discriminators_list:
            if error := _validate_discriminators(discriminators_list):
                return error, schemas
            prop = evolve(prop, discriminators=discriminators_list)

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

    def _get_inner_type_strings(self, json: bool, multipart: bool) -> set[str]:
        return {
            p.get_type_string(no_optional=True, json=json, multipart=multipart, quoted=not p.is_base_type)
            for p in self.inner_properties
        }

    @staticmethod
    def _get_type_string_from_inner_type_strings(inner_types: set[str]) -> str:
        if len(inner_types) == 1:
            return inner_types.pop()
        return f"Union[{', '.join(sorted(inner_types))}]"

    def get_base_type_string(self, *, quoted: bool = False) -> str:
        return self._get_type_string_from_inner_type_strings(self._get_inner_type_strings(json=False, multipart=False))

    def get_base_json_type_string(self, *, quoted: bool = False) -> str:
        return self._get_type_string_from_inner_type_strings(self._get_inner_type_strings(json=True, multipart=False))

    def get_type_strings_in_union(self, *, no_optional: bool = False, json: bool, multipart: bool) -> set[str]:
        """
        Get the set of all the types that should appear within the `Union` representing this property.

        This function is called from the union property macros, thus the public visibility.

        Args:
            no_optional: Do not include `None` or `Unset` in this set.
            json: If True, this returns the JSON types, not the Python types, of this property.
            multipart: If True, this returns the multipart types, not the Python types, of this property.

        Returns:
            A set of strings containing the types that should appear within `Union`.
        """
        type_strings = self._get_inner_type_strings(json=json, multipart=multipart)
        if no_optional:
            return type_strings
        if not self.required:
            type_strings.add("Unset")
        return type_strings

    def get_type_string(
        self,
        no_optional: bool = False,
        json: bool = False,
        *,
        multipart: bool = False,
        quoted: bool = False,
    ) -> str:
        """
        Get a string representation of type that should be used when declaring this property.
        This implementation differs slightly from `Property.get_type_string` in order to collapse
        nested union types.
        """
        type_strings_in_union = self.get_type_strings_in_union(no_optional=no_optional, json=json, multipart=multipart)
        return self._get_type_string_from_inner_type_strings(type_strings_in_union)

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
        imports.add("from typing import cast, Union")
        return imports

    def get_lazy_imports(self, *, prefix: str) -> set[str]:
        lazy_imports = super().get_lazy_imports(prefix=prefix)
        for inner_prop in self.inner_properties:
            lazy_imports.update(inner_prop.get_lazy_imports(prefix=prefix))
        return lazy_imports

    def validate_location(self, location: oai.ParameterLocation) -> ParseError | None:
        """Returns an error if this type of property is not allowed in the given location"""
        from ..properties import Property

        for inner_prop in self.inner_properties:
            if evolve(cast(Property, inner_prop), required=self.required).validate_location(location) is not None:
                return ParseError(detail=f"{self.get_type_string()} is not allowed in {location}")
        return None


def _flatten_union_properties(
    sub_properties: list[PropertyProtocol],
) -> tuple[list[PropertyProtocol], list[DiscriminatorDefinition]]:
    flattened = []
    discriminators = []
    for sub_prop in sub_properties:
        if isinstance(sub_prop, UnionProperty):
            if sub_prop.discriminators:
                discriminators.extend(sub_prop.discriminators)
            new_props, new_discriminators = _flatten_union_properties(sub_prop.inner_properties)
            flattened.extend(new_props)
            discriminators.extend(new_discriminators)
        else:
            flattened.append(sub_prop)
    return flattened, discriminators


def _parse_discriminator(
    data: oai.Discriminator,
    subtypes: list[PropertyProtocol],
    schemas: Schemas,
) -> DiscriminatorDefinition | PropertyError:
    from .model_property import ModelProperty

    # See: https://spec.openapis.org/oas/v3.1.0.html#discriminator-object

    def _find_top_level_model(matching_model: ModelProperty) -> ModelProperty | None:
        # This is needed because, when we built the union list, $refs were changed into a copy of
        # the type they referred to, without preserving the original name. We need to know that
        # every type in the discriminator is a $ref to a top-level type and we need its name.
        for prop in schemas.classes_by_reference.values():
            if isinstance(prop, ModelProperty):
                if prop.class_info == matching_model.class_info:
                    return prop
        return None

    model_types_by_name: dict[str, PropertyProtocol] = {}
    for model in subtypes:
        # Note, model here can never be a UnionProperty, because we've already done
        # flatten_union_properties() before this point.
        if not isinstance(model, ModelProperty):
            return PropertyError(
                detail="All schema variants must be objects when using a discriminator",
            )
        top_level_model = _find_top_level_model(model)
        if not top_level_model:
            return PropertyError(
                detail="Inline schema declarations are not allowed when using a discriminator",
            )
        name = top_level_model.name
        if name.startswith("/components/schemas/"):
            name = get_reference_simple_name(name)
        model_types_by_name[name] = top_level_model

    # The discriminator can specify an explicit mapping of values to types, but it doesn't
    # have to; the default behavior is that the value for each type is simply its name.
    mapping: dict[str, PropertyProtocol] = model_types_by_name.copy()
    if data.mapping:
        for discriminator_value, model_ref in data.mapping.items():
            ref_path = parse_reference_path(
                model_ref if model_ref.startswith("#/components/schemas/") else f"#/components/schemas/{model_ref}"
            )
            if isinstance(ref_path, ParseError) or ref_path not in schemas.classes_by_reference:
                return PropertyError(detail=f'Invalid reference "{model_ref}" in discriminator mapping')
            name = get_reference_simple_name(ref_path)
            if not (lookup_model := model_types_by_name.get(name)):
                return PropertyError(
                    detail=f'Discriminator mapping referred to "{model_ref}" which is not one of the schema variants',
                )
            for original_value in (name for name, m in model_types_by_name.items() if m == lookup_model):
                mapping.pop(original_value)
            mapping[discriminator_value] = lookup_model
    else:
        mapping = model_types_by_name

    return DiscriminatorDefinition(property_name=data.propertyName, value_to_model_map=mapping)


def _validate_discriminators(
    discriminators: list[DiscriminatorDefinition],
) -> PropertyError | None:
    from .model_property import ModelProperty

    prop_names_values_classes = [
        (discriminator.property_name, key, cast(ModelProperty, model).class_info.name)
        for discriminator in discriminators
        for key, model in discriminator.value_to_model_map.items()
    ]
    for p, v in {(p, v) for p, v, _ in prop_names_values_classes}:
        if len({c for p1, v1, c in prop_names_values_classes if (p1, v1) == (p, v)}) > 1:
            return PropertyError(f'Discriminator property "{p}" had more than one schema for value "{v}"')
    return None

    # TODO: We should also validate that property_name refers to a property that 1. exists,
    # 2. is required, 3. is a string (in all of these models). However, currently we can't
    # do that because, at the time this function is called, the ModelProperties within the
    # union haven't yet been post-processed and so we don't have full information about
    # their properties. To fix this, we may need to generalize the post-processing phase so
    # that any Property type, not just ModelProperty, can say it needs post-processing; then
    # we can defer _validate_discriminators till that phase.
