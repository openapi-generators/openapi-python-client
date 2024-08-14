
from collections.abc import Callable
from typing import Any

from attr import evolve

from openapi_python_client.parser.properties.any import AnyProperty
from openapi_python_client.parser.properties.enum_property import EnumProperty, ValueType
from openapi_python_client.parser.properties.float import FloatProperty
from openapi_python_client.parser.properties.int import IntProperty
from openapi_python_client.parser.properties.list_property import ListProperty
from openapi_python_client.parser.properties.protocol import PropertyProtocol
from openapi_python_client.parser.properties.string import StringProperty


def merge_properties(prop1: PropertyProtocol, prop2: PropertyProtocol) -> PropertyProtocol:
    """Attempt to create a new property that incorporates the behavior of both.
    
    This is used when merging schemas with allOf, when two schemas define a property with the same name.
    
    OpenAPI defines allOf in terms of validation behavior: the input must pass the validation rules
    defined in all of the listed schemas. Our task here is slightly more difficult, since we must end
    up with a single Property object that will be used to generate a single class property in the
    generated code. Due to limitations of our internal model, this may not be possible for some
    combinations of property attributes that OpenAPI supports (for instance, we have no way to represent
    a string property that must match two different regexes).

    Properties can also have attributes that do not represent validation rules, such as "description"
    and "example". OpenAPI does not define any overriding/aggregation rules for these in allOf. The
    implementation here is, assuming prop1 and prop2 are in the same order that the schemas were in the
    allOf, any such attributes that prop2 specifies will override the ones from prop1.

    Any failure is thrown as a ValueError.
    """
    if isinstance(prop1, EnumProperty) or isinstance(prop2, EnumProperty):
        return _merge_with_enum(prop1, prop2)

    if prop1.__class__ == prop2.__class__:
        return _merge_same_type(prop1, prop2)
    
    if isinstance(prop1, AnyProperty) or isinstance(prop2, AnyProperty):
        return _merge_with_any(prop1, prop2)
    
    if _is_numeric(prop1) and _is_numeric(prop2):
        return _merge_numeric(prop1, prop2)

    raise ValueError("defined with two incompatible types")


def _is_numeric(prop: PropertyProtocol) -> bool:
    return isinstance(prop, IntProperty) or isinstance(prop, FloatProperty)


def _merge_same_type(prop1: PropertyProtocol, prop2: PropertyProtocol) -> PropertyProtocol:
    if prop1 == prop2:
        # It's always OK to redefine a property with everything exactly the same
        return prop1

    if isinstance(prop1, StringProperty):
        return _merge_string(prop1, prop2)

    if isinstance(prop1, ListProperty):
        # There's no clear way to represent the intersection of two different list types. Fail in this case.
        if prop1.inner_property != prop2.inner_property:
            raise ValueError("can't redefine a list property with a different element type")

    # For all other property types, there aren't any special attributes that affect validation, so just
    # apply the rules for common attributes like "description".
    return _merge_common_attributes(prop1, prop2)


def _merge_string(prop1: StringProperty, prop2: StringProperty) -> StringProperty:
    # If max_length was specified for both, the smallest value takes precedence. If only one of them
    # specifies it, _combine_values will pick that one.
    max_length: int | None = _combine_values(prop1.max_length, prop2.max_length, lambda a, b: min([a, b]))

    # If pattern was specified for both, we have a problem. OpenAPI has no logical objection to this;
    # it would just mean the value must match both of the patterns to be valid. But we have no way to
    # represent this in our internal model currently.
    pattern: str | None | ValueError = _combine_values(
        prop1.pattern,
        prop2.pattern,
        lambda a, b: ValueError("specified two different regex patterns")
    )
    if isinstance(pattern, ValueError):
        raise pattern
    
    return _merge_common_attributes(evolve(prop1, max_length=max_length, pattern=pattern), prop2)


def _merge_numeric(prop1: PropertyProtocol, prop2: PropertyProtocol) -> IntProperty:
    # Here, one of the properties was defined as "int" and the other was just a general number (which
    # we call FloatProperty). "Must be integer" is the stricter validation rule, so the result must be
    # an IntProperty.
    int_prop = prop1 if isinstance(prop1, IntProperty) else prop2
    result = _merge_common_attributes(int_prop, prop1, prop2)
    if result.default is not None:
        if isinstance(result.default, float) and not result.default.is_integer():
            raise ValueError(f"default value {result.default} is not valid for an integer property")
    return result
    

def _merge_with_any(prop1: PropertyProtocol, prop2: PropertyProtocol) -> PropertyProtocol:
    # AnyProperty implies no validation rules for a value, so merging it with any other type just means
    # we should use the validation rules for the other type and the result should not be an AnyProperty.
    non_any_prop = prop2 if isinstance(prop1, AnyProperty) else prop1
    return _merge_common_attributes(non_any_prop, prop1, prop2)


def _merge_with_enum(prop1: PropertyProtocol, prop2: PropertyProtocol) -> EnumProperty:
    if isinstance(prop1, EnumProperty) and isinstance(prop2, EnumProperty):
        # We want the narrowest validation rules that fit both, so use whichever values list is a
        # subset of the other.
        values: dict[str, ValueType]
        if _values_are_subset(prop1, prop2):
            values = prop1.values
        elif _values_are_subset(prop2, prop1):
            values = prop2.values
        else:
            raise ValueError("can't redefine an enum property with incompatible lists of values")
        return _merge_common_attributes(evolve(prop1, values=values), prop2)

    # If enum values were specified for just one of the properties, use those.
    enum_prop = prop1 if isinstance(prop1, EnumProperty) else prop2
    non_enum_prop = prop2 if isinstance(prop1, EnumProperty) else prop1
    if (
        (isinstance(non_enum_prop, IntProperty) and enum_prop.value_type is int) or
        (isinstance(non_enum_prop, StringProperty) and enum_prop.value_type is str)
    ):
        return _merge_common_attributes(enum_prop, prop1, prop2)
    raise ValueError("defined with two incompatible types")


def _merge_common_attributes(base: PropertyProtocol, *extend_with: PropertyProtocol) -> PropertyProtocol:
    """Create a new instance based on base, overriding basic attributes with values from extend_with, in order.
    
    For "default", "description", and "example", a non-None value overrides any value from a previously
    specified property. The behavior is similar to using the spread operator with dictionaries, except
    that None means "not specified".

    For "required", any True value overrides all other values (a property that was previously required
    cannot become optional).
    """
    current = base
    for override in extend_with:
        current = evolve(
            current,
            required=current.required or override.required,
            default = override.default or current.default,
            description = override.description or current.description,
            example = override.example or current.example,
    )
    return current


def _values_are_subset(prop1: EnumProperty, prop2: EnumProperty) -> bool:
    return set(prop1.values.items()) <= set(prop2.values.items())


def _combine_values(value1: Any, value2: Any, combinator: Callable) -> Any:
    if value1 == value2:
        return value1
    if value1 is None:
        return value2
    if value2 is None:
        return value1
    return combinator(value1, value2)
