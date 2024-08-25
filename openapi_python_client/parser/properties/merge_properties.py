from __future__ import annotations

__all__ = ["merge_properties"]

from typing import TYPE_CHECKING, Any, Callable, TypeVar, cast

from attr import evolve

from . import FloatProperty
from .any import AnyProperty
from .enum_property import EnumProperty, ValueType
from .int import IntProperty
from .list_property import ListProperty
from .protocol import PropertyProtocol
from .schemas import Class
from .string import StringProperty

if TYPE_CHECKING:
    from .property import Property
else:
    Property = "Property"

PropertyT = TypeVar("PropertyT", bound=PropertyProtocol)


def merge_properties(prop1: Property, prop2: Property) -> Property:
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

    Any failure is thrown as a ValueError.
    """
    if isinstance(prop2, AnyProperty):
        return _merge_common_attributes(prop1, prop2)

    if isinstance(prop1, AnyProperty):
        # Use the base type of `prop2`, but keep the override order
        return _merge_common_attributes(prop2, prop1, prop2)

    if isinstance(prop1, EnumProperty) or isinstance(prop2, EnumProperty):
        return _merge_with_enum(prop1, prop2)

    if (merged := _merge_same_type(prop1, prop2)) is not None:
        return merged

    if (merged := _merge_numeric(prop1, prop2)) is not None:
        return merged

    raise ValueError("defined with two incompatible types")


def _merge_same_type(prop1: Property, prop2: Property) -> Property | None:
    if type(prop1) is not type(prop2):
        return None

    if prop1 == prop2:
        # It's always OK to redefine a property with everything exactly the same
        return prop1

    if isinstance(prop1, StringProperty) and isinstance(prop2, StringProperty):
        return _merge_string(prop1, prop2)

    if isinstance(prop1, ListProperty) and isinstance(prop2, ListProperty):
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
        prop1.pattern, prop2.pattern, lambda a, b: ValueError("specified two different regex patterns")
    )
    if isinstance(pattern, ValueError):
        raise pattern

    return _merge_common_attributes(evolve(prop1, max_length=max_length, pattern=pattern), prop2)


def _merge_numeric(prop1: Property, prop2: Property) -> IntProperty | None:
    """Merge IntProperty with FloatProperty"""
    if isinstance(prop1, IntProperty) and isinstance(prop2, (IntProperty, FloatProperty)):
        result = _merge_common_attributes(prop1, prop2)
    elif isinstance(prop2, IntProperty) and isinstance(prop1, (IntProperty, FloatProperty)):
        # Use the IntProperty as a base since it's more restrictive, but keep the correct override order
        result = _merge_common_attributes(prop2, prop1, prop2)
    else:
        return None
    if result.default is not None:
        if isinstance(result.default, float) and not result.default.is_integer():
            raise ValueError(f"default value {result.default} is not valid for an integer property")
    return result


def _merge_with_enum(prop1: PropertyProtocol, prop2: PropertyProtocol) -> EnumProperty:
    if isinstance(prop1, EnumProperty) and isinstance(prop2, EnumProperty):
        # We want the narrowest validation rules that fit both, so use whichever values list is a
        # subset of the other.
        values: dict[str, ValueType]
        class_info: Class
        if _values_are_subset(prop1, prop2):
            values = prop1.values
            class_info = prop1.class_info
        elif _values_are_subset(prop2, prop1):
            values = prop2.values
            class_info = prop2.class_info
        else:
            raise ValueError("can't redefine an enum property with incompatible lists of values")
        return _merge_common_attributes(evolve(prop1, values=values, class_info=class_info), prop2)

    # If enum values were specified for just one of the properties, use those.
    enum_prop = prop1 if isinstance(prop1, EnumProperty) else cast(EnumProperty, prop2)
    non_enum_prop = prop2 if isinstance(prop1, EnumProperty) else prop1
    if (isinstance(non_enum_prop, IntProperty) and enum_prop.value_type is int) or (
        isinstance(non_enum_prop, StringProperty) and enum_prop.value_type is str
    ):
        return _merge_common_attributes(enum_prop, prop1, prop2)
    raise ValueError("defined with two incompatible types")


def _merge_common_attributes(base: PropertyT, *extend_with: PropertyProtocol) -> PropertyT:
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
            current,  # type: ignore # can't prove that every property type is an attrs class, but it is
            required=current.required or override.required,
            default=override.default or current.default,
            description=override.description or current.description,
            example=override.example or current.example,
        )
    return current


def _values_are_subset(prop1: EnumProperty, prop2: EnumProperty) -> bool:
    return set(prop1.values.items()) <= set(prop2.values.items())


def _combine_values(value1: Any, value2: Any, combinator: Callable[[Any, Any], Any]) -> Any:
    if value1 == value2:
        return value1
    if value1 is None:
        return value2
    if value2 is None:
        return value1
    return combinator(value1, value2)
