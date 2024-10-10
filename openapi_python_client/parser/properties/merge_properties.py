from __future__ import annotations
from itertools import chain

from openapi_python_client import utils
from openapi_python_client.config import Config
from openapi_python_client.parser.properties.date import DateProperty
from openapi_python_client.parser.properties.datetime import DateTimeProperty
from openapi_python_client.parser.properties.file import FileProperty
from openapi_python_client.parser.properties.model_property import ModelDetails, ModelProperty, _gather_property_data
from openapi_python_client.parser.properties.schemas import Class, Schemas

__all__ = ["merge_properties"]

from typing import TypeVar, cast

from attr import evolve

from ..errors import PropertyError
from . import FloatProperty
from .any import AnyProperty
from .enum_property import EnumProperty
from .int import IntProperty
from .list_property import ListProperty
from .property import Property
from .protocol import PropertyProtocol
from .string import StringProperty

PropertyT = TypeVar("PropertyT", bound=PropertyProtocol)


STRING_WITH_FORMAT_TYPES = (DateProperty, DateTimeProperty, FileProperty)


def merge_properties(
    prop1: Property,
    prop2: Property,
    parent_name: str,
    config: Config,
) -> Property | PropertyError:  # noqa: PLR0911
    """Attempt to create a new property that incorporates the behavior of both.

    This is used when merging schemas with allOf, when two schemas define a property with the same name.

    OpenAPI defines allOf in terms of validation behavior: the input must pass the validation rules
    defined in all the listed schemas. Our task here is slightly more difficult, since we must end
    up with a single Property object that will be used to generate a single class property in the
    generated code. Due to limitations of our internal model, this may not be possible for some
    combinations of property attributes that OpenAPI supports (for instance, we have no way to represent
    a string property that must match two different regexes).

    Properties can also have attributes that do not represent validation rules, such as "description"
    and "example". OpenAPI does not define any overriding/aggregation rules for these in allOf. The
    implementation here is, assuming prop1 and prop2 are in the same order that the schemas were in the
    allOf, any such attributes that prop2 specifies will override the ones from prop1.
    """
    if isinstance(prop2, AnyProperty):
        return _merge_common_attributes(prop1, prop2)

    if isinstance(prop1, AnyProperty):
        # Use the base type of `prop2`, but keep the override order
        return _merge_common_attributes(prop2, prop1, prop2)

    if isinstance(prop1, EnumProperty) or isinstance(prop2, EnumProperty):
        return _merge_with_enum(prop1, prop2)

    if (merged := _merge_same_type(prop1, prop2, parent_name, config)) is not None:
        return merged

    if (merged := _merge_numeric(prop1, prop2)) is not None:
        return merged

    if (merged := _merge_string_with_format(prop1, prop2)) is not None:
        return merged

    return PropertyError(
        detail=f"{prop1.get_type_string(no_optional=True)} can't be merged with {prop2.get_type_string(no_optional=True)}"
    )


def _merge_same_type(prop1: Property, prop2: Property, parent_name: str, config: Config) -> Property | None | PropertyError:
    if type(prop1) is not type(prop2):
        return None

    if prop1 == prop2:
        # It's always OK to redefine a property with everything exactly the same
        return prop1

    if isinstance(prop1, ModelProperty) and isinstance(prop2, ModelProperty):
        return _merge_models(prop1, prop2, parent_name, config)

    if isinstance(prop1, ListProperty) and isinstance(prop2, ListProperty):
        inner_property = merge_properties(prop1.inner_property, prop2.inner_property, "", config)  # type: ignore
        if isinstance(inner_property, PropertyError):
            return PropertyError(detail=f"can't merge list properties: {inner_property.detail}")
        prop1.inner_property = inner_property

    # For all other property types, there aren't any special attributes that affect validation, so just
    # apply the rules for common attributes like "description".
    return _merge_common_attributes(prop1, prop2)


def _merge_models(prop1: ModelProperty, prop2: ModelProperty, parent_name: str, config: Config) -> Property | PropertyError:
    # Ideally, we would treat this case the same as a schema that consisted of "allOf: [prop1, prop2]",
    # applying the property merge logic recursively and creating a new third schema if the result could
    # not be fully described by one or the other. But for now we will just handle the common case where
    # B is an object type that extends A and fully includes it, with no changes to any of A's properties;
    # in that case, it is valid to just reuse the model class for B.
    for prop in [prop1, prop2]:
        if prop.needs_processing():
            # This means not all of the details of the schema have been filled in, possibly due to a
            # forward reference. That may be resolved in a later pass, but for now we can't proceed.
            return PropertyError(f"Schema for {prop} in allOf was not processed", data=prop)

    # Detect whether one of the schemas is derived from the other-- that is, if it is (or is equivalent
    # to) the result of taking the other type and adding/modifying properties with allOf. If so, then
    # we can simply use the class of the derived type. We will still call _merge_common_attributes in
    # case any metadata like "description" has been modified.
    if _model_is_extension_of(prop1, prop2, parent_name, config):
        return _merge_common_attributes(prop1, prop2)
    elif _model_is_extension_of(prop2, prop1, parent_name, config):
        return _merge_common_attributes(prop2, prop1, prop2)

    # Neither of the schemas is a superset of the other, so merging them will result in a new type.
    merged_props: dict[str, Property] = {p.name: p for p in chain(prop1.required_properties, prop1.optional_properties)}
    for model in [prop1, prop2]:
        for sub_prop in chain(model.required_properties, model.optional_properties):
            if sub_prop.name in merged_props:
                merged_prop = merge_properties(merged_props[sub_prop.name], sub_prop, parent_name, config)
                if isinstance(merged_prop, PropertyError):
                    return merged_prop
                merged_props[sub_prop.name] = merged_prop
            else:
                merged_props[sub_prop.name] = sub_prop
    
    prop_data = _gather_property_data(merged_props.values(), Schemas())
    
    name = prop2.name
    class_string = f"{utils.pascal_case(parent_name)}{utils.pascal_case(name)}"
    class_info = Class.from_string(string=class_string, config=config)
    roots = prop1.roots.union(prop2.roots).difference({prop1.class_info.name, prop2.class_info.name})
    roots.add(class_info.name)
    prop_details = ModelDetails(
        required_properties=prop_data.required_props,
        optional_properties=prop_data.optional_props,
        additional_properties=None,
        relative_imports=prop_data.relative_imports,
        lazy_imports=prop_data.lazy_imports,
    )
    prop = ModelProperty(
        class_info=class_info,
        data=prop2.data,  # TODO: not sure what this should be
        roots=roots,
        details=prop_details,
        description=prop2.description or prop1.description,
        default=None,
        required=prop2.required or prop1.required,
        name=name,
        python_name=utils.PythonIdentifier(value=name, prefix=config.field_prefix),
        example=prop2.example or prop1.example,
    )

    return prop


def _merge_string_with_format(prop1: Property, prop2: Property) -> Property | None | PropertyError:
    """Merge a string that has no format with a string that has a format"""
    # Here we need to use the DateProperty/DateTimeProperty/FileProperty as the base so that we preserve
    # its class, but keep the correct override order for merging the attributes.
    if isinstance(prop1, StringProperty) and isinstance(prop2, STRING_WITH_FORMAT_TYPES):
        # Use the more specific class as a base, but keep the correct override order
        return _merge_common_attributes(prop2, prop1, prop2)
    elif isinstance(prop2, StringProperty) and isinstance(prop1, STRING_WITH_FORMAT_TYPES):
        return _merge_common_attributes(prop1, prop2)
    else:
        return None


def _merge_numeric(prop1: Property, prop2: Property) -> IntProperty | None | PropertyError:
    """Merge IntProperty with FloatProperty"""
    if isinstance(prop1, IntProperty) and isinstance(prop2, (IntProperty, FloatProperty)):
        return _merge_common_attributes(prop1, prop2)
    elif isinstance(prop2, IntProperty) and isinstance(prop1, (IntProperty, FloatProperty)):
        # Use the IntProperty as a base since it's more restrictive, but keep the correct override order
        return _merge_common_attributes(prop2, prop1, prop2)
    else:
        return None


def _merge_with_enum(prop1: PropertyProtocol, prop2: PropertyProtocol) -> EnumProperty | PropertyError:
    if isinstance(prop1, EnumProperty) and isinstance(prop2, EnumProperty):
        # We want the narrowest validation rules that fit both, so use whichever values list is a
        # subset of the other.
        if _values_are_subset(prop1, prop2):
            values = prop1.values
            class_info = prop1.class_info
        elif _values_are_subset(prop2, prop1):
            values = prop2.values
            class_info = prop2.class_info
        else:
            return PropertyError(detail="can't redefine an enum property with incompatible lists of values")
        return _merge_common_attributes(evolve(prop1, values=values, class_info=class_info), prop2)

    # If enum values were specified for just one of the properties, use those.
    enum_prop = prop1 if isinstance(prop1, EnumProperty) else cast(EnumProperty, prop2)
    non_enum_prop = prop2 if isinstance(prop1, EnumProperty) else prop1
    if (isinstance(non_enum_prop, IntProperty) and enum_prop.value_type is int) or (
        isinstance(non_enum_prop, StringProperty) and enum_prop.value_type is str
    ):
        return _merge_common_attributes(enum_prop, prop1, prop2)
    return PropertyError(
        detail=f"can't combine enum of type {enum_prop.value_type} with {non_enum_prop.get_type_string(no_optional=True)}"
    )


def _merge_common_attributes(base: PropertyT, *extend_with: PropertyProtocol) -> PropertyT | PropertyError:
    """Create a new instance based on base, overriding basic attributes with values from extend_with, in order.

    For "default", "description", and "example", a non-None value overrides any value from a previously
    specified property. The behavior is similar to using the spread operator with dictionaries, except
    that None means "not specified".

    For "required", any True value overrides all other values (a property that was previously required
    cannot become optional).
    """
    current = base
    for override in extend_with:
        if override.default is not None:
            override_default = current.convert_value(override.default.raw_value)
        else:
            override_default = None
        if isinstance(override_default, PropertyError):
            return override_default
        current = evolve(
            current,  # type: ignore # can't prove that every property type is an attrs class, but it is
            required=current.required or override.required,
            default=override_default or current.default,
            description=override.description or current.description,
            example=override.example or current.example,
        )
    return current


def _values_are_subset(prop1: EnumProperty, prop2: EnumProperty) -> bool:
    return set(prop1.values.items()) <= set(prop2.values.items())


def _model_is_extension_of(extended_model: ModelProperty, base_model: ModelProperty, parent_name: str, config: Config) -> bool:
    def _properties_are_extension_of(extended_list: list[Property], base_list: list[Property]) -> bool:
        for p2 in base_list:
            if not [p1 for p1 in extended_list if _property_is_extension_of(p2, p1, parent_name, config)]:
                return False
        return True

    return _properties_are_extension_of(
        extended_model.required_properties, base_model.required_properties
    ) and _properties_are_extension_of(extended_model.optional_properties, base_model.optional_properties)


def _property_is_extension_of(extended_prop: PropertyProtocol, base_prop: PropertyProtocol, parent_name: str, config: Config) -> bool:
    return base_prop.name == extended_prop.name and (
        base_prop == extended_prop or merge_properties(base_prop, extended_prop, parent_name, config) == extended_prop
    )
