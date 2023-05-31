from typing import Dict, Optional, Tuple, Set

from .properties import ModelProperty, ListProperty, Property


def traverse_properties(
    property_obj: Property,
    path: Tuple[str, ...] = (),
    list_properties: Optional[Dict[Tuple[str, ...], ModelProperty]] = None,
    model_properties: Optional[Dict[Tuple[str, ...], ModelProperty]] = None,
    seen: Optional[Set[str]] = None,
) -> Tuple[Dict[Tuple[str, ...], ModelProperty], Dict[Tuple[str, ...], ModelProperty]]:
    """
    Recursively traverse a ModelProperty or ListProperty object to generate mappings of:

    a. All ListProperty objects which contain models (arrays of objects in openapi)
    b. All ModelProperty descendents of the property

    The result is a tuple of two dicts with json paths as keys and `ModelProperty` objects as values.

    :param property_obj: The ModelProperty or ListProperty object to traverse.
    :param path: The current path, used for constructing the path to each property.
    :param list_properties: Optional. A dictionary to store the paths referencing ListProperty
                            objects with ModelProperty as their inner property.
    :param model_properties: Optional. A dictionary to store the paths referencing ModelProperty objects.
    :return: A tuple containing two dictionaries, mapping jsonpaths to ModelProperty objects
    """
    if list_properties is None:
        list_properties = {}
    if model_properties is None:
        model_properties = {}
    if seen is None:
        seen = set()

    if isinstance(property_obj, ModelProperty):
        # Avoid infinite self referencing call cycles
        if property_obj.class_info.name in seen:
            return list_properties, model_properties
        seen.add(property_obj.class_info.name)
        model_properties[path] = property_obj
        for prop in property_obj.optional_properties or []:
            if isinstance(prop, (ModelProperty, ListProperty)):
                traverse_properties(prop, path + (prop.name,), list_properties, model_properties, seen)
        for prop in property_obj.required_properties or []:
            if isinstance(prop, (ModelProperty, ListProperty)):
                traverse_properties(prop, path + (prop.name,), list_properties, model_properties, seen)

    elif isinstance(property_obj, ListProperty) and isinstance(property_obj.inner_property, ModelProperty):
        inner = property_obj.inner_property
        list_properties[path] = inner
        traverse_properties(inner, path + ("[*]",), list_properties, model_properties, seen)

    return list_properties, model_properties
