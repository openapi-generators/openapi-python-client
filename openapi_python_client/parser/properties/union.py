from __future__ import annotations

from itertools import chain
from typing import Any, ClassVar, Mapping, OrderedDict, cast

from attr import define, evolve

from ... import Config
from ... import schema as oai
from ...utils import PythonIdentifier
from ..errors import ParseError, PropertyError
from .protocol import PropertyProtocol, Value
from .schemas import Schemas, get_reference_simple_name, parse_reference_path


@define
class DiscriminatorDefinition:
    """Represents a discriminator that can optionally be specified for a union type.

    Normally, a UnionProperty has either zero or one of these. However, a nested union
    could have more than one, as we accumulate all the discriminators when we flatten
    out the nested schemas. For example:

        anyOf:
          - anyOf:
              - $ref: "#/components/schemas/Cat"
              - $ref: "#/components/schemas/Dog"
            discriminator:
              propertyName: mammalType
          - anyOf:
              - $ref: "#/components/schemas/Condor"
              - $ref: "#/components/schemas/Chicken"
            discriminator:
              propertyName: birdType

    In this example there are four schemas and two discriminators. The deserializer
    logic will check for the mammalType property first, then birdType.
    """

    property_name: str
    value_to_model_map: Mapping[str, PropertyProtocol]
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

        sub_properties, discriminators_from_nested_unions = _flatten_union_properties(sub_properties)

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

        all_discriminators = discriminators_from_nested_unions
        if data.discriminator:
            discriminator_or_error = _parse_discriminator(data.discriminator, sub_properties, schemas)
            if isinstance(discriminator_or_error, PropertyError):
                return discriminator_or_error, schemas
            all_discriminators = [discriminator_or_error, *all_discriminators]
        if all_discriminators:
            prop = evolve(prop, discriminators=all_discriminators)

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

    # Conditions that must be true when there is a discriminator:
    # 1. Every type in the anyOf/oneOf list must be a $ref to a named schema, such as
    #    #/components/schemas/X, rather than an inline schema. This is important because
    #    we may need to use the schema's simple name (X).
    # 2. There must be a propertyName, representing a property that exists in every
    #    schema in that list (although we can't currently enforce the latter condition,
    #    because those properties haven't been parsed yet at this point.)
    #
    # There *may* also be a mapping of lookup values (the possible values of the property)
    # to schemas. Schemas can be referenced either by a full path or a name:
    #      mapping:
    #        value_for_a: "#/components/schemas/ModelA"
    #        value_for_b: ModelB   # equivalent to "#/components/schemas/ModelB"
    #
    # For any type that isn't specified in the mapping (or if the whole mapping is omitted)
    # the default lookup value for each schema is the same as the schema name. So this--
    #      mapping:
    #        value_for_a: "#/components/schemas/ModelA"
    # --is exactly equivalent to this:
    #    discriminator:
    #      propertyName: modelType
    #      mapping:
    #        value_for_a: "#/components/schemas/ModelA"
    #        ModelB: "#/components/schemas/ModelB"

    def _get_model_name(model: ModelProperty) -> str | None:
        return get_reference_simple_name(model.ref_path) if model.ref_path else None

    model_types_by_name: dict[str, ModelProperty] = {}
    for model in subtypes:
        # Note, model here can never be a UnionProperty, because we've already done
        # flatten_union_properties() before this point.
        if not isinstance(model, ModelProperty):
            return PropertyError(
                detail="All schema variants must be objects when using a discriminator",
            )
        name = _get_model_name(model)
        if not name:
            return PropertyError(
                detail="Inline schema declarations are not allowed when using a discriminator",
            )
        model_types_by_name[name] = model

    mapping: dict[str, ModelProperty] = OrderedDict()  # use ordered dict for test determinacy
    unspecified_models = list(model_types_by_name.values())
    if data.mapping:
        for discriminator_value, model_ref in data.mapping.items():
            if "/" in model_ref:
                ref_path = parse_reference_path(model_ref)
                if isinstance(ref_path, ParseError) or ref_path not in schemas.classes_by_reference:
                    return PropertyError(detail=f'Invalid reference "{model_ref}" in discriminator mapping')
                name = get_reference_simple_name(ref_path)
            else:
                name = model_ref
            mapped_model = model_types_by_name.get(name)
            if not mapped_model:
                return PropertyError(
                    detail=f'Discriminator mapping referred to "{name}" which is not one of the schema variants',
                )
            mapping[discriminator_value] = mapped_model
            if mapped_model in unspecified_models:
                # could've already been removed if more than one value is mapped to the same model
                unspecified_models.remove(mapped_model)
    for model in unspecified_models:
        if name := _get_model_name(model):
            mapping[name] = model
    return DiscriminatorDefinition(property_name=data.propertyName, value_to_model_map=mapping)
