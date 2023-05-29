from itertools import chain
from typing import ClassVar, List, Set, Tuple, Union

import attr

from ... import schema as oai
from ... import utils
from ...config import Config
from ..errors import PropertyError
from .converter import convert_chain
from .property import Property
from .schemas import Schemas


@attr.s(auto_attribs=True, frozen=True)
class UnionProperty(Property):
    """A property representing a Union (anyOf) of other properties"""

    inner_properties: List[Property]
    template: ClassVar[str] = "union_property.py.jinja"

    def _get_inner_type_strings(self, json: bool = False) -> Set[str]:
        return {
            p.get_type_string(no_optional=True, json=json, quoted=not p.is_base_type) for p in self.inner_properties
        }

    @staticmethod
    def _get_type_string_from_inner_type_strings(inner_types: Set[str]) -> str:
        if len(inner_types) == 1:
            return inner_types.pop()
        return f"Union[{', '.join(sorted(inner_types))}]"

    # pylint: disable=unused-argument
    def get_base_type_string(self, *, quoted: bool = False) -> str:
        return self._get_type_string_from_inner_type_strings(self._get_inner_type_strings(json=False))

    def get_base_json_type_string(self, *, quoted: bool = False) -> str:
        return self._get_type_string_from_inner_type_strings(self._get_inner_type_strings(json=True))

    def get_type_strings_in_union(self, no_optional: bool = False, json: bool = False) -> Set[str]:
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
        if self.nullable:
            type_strings.add("None")
        if not self.required:
            type_strings.add("Unset")
        return type_strings

    def get_type_string(
        self,
        no_optional: bool = False,
        json: bool = False,
        *,
        quoted: bool = False,
    ) -> str:
        """
        Get a string representation of type that should be used when declaring this property.
        This implementation differs slightly from `Property.get_type_string` in order to collapse
        nested union types.
        """
        type_strings_in_union = self.get_type_strings_in_union(no_optional=no_optional, json=json)
        return self._get_type_string_from_inner_type_strings(type_strings_in_union)

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

    def get_lazy_imports(self, *, prefix: str) -> Set[str]:
        lazy_imports = super().get_lazy_imports(prefix=prefix)
        for inner_prop in self.inner_properties:
            lazy_imports.update(inner_prop.get_lazy_imports(prefix=prefix))
        return lazy_imports


def build_union_property(
    *, data: oai.Schema, name: str, required: bool, schemas: Schemas, parent_name: str, config: Config
) -> Tuple[Union[UnionProperty, PropertyError], Schemas]:
    """
    Create a `UnionProperty` the right way.

    Args:
        data: The `Schema` describing the `UnionProperty`.
        name: The name of the property where it appears in the OpenAPI document.
        required: Whether or not this property is required where it's being used.
        schemas: The `Schemas` so far describing existing classes / references.
        parent_name: The name of the thing which holds this property (used for renaming inner classes).
        config: User-defined config values for modifying inner properties.

    Returns:
        `(result, schemas)` where `schemas` is the updated version of the input `schemas` and `result` is the
            constructed `UnionProperty` or a `PropertyError` describing what went wrong.
    """
    sub_properties: List[Property] = []
    from .build import property_from_data  # TODO: Circular import

    for i, sub_prop_data in enumerate(chain(data.anyOf, data.oneOf)):
        sub_prop, schemas = property_from_data(
            name=f"{name}_type_{i}",
            required=required,
            data=sub_prop_data,
            schemas=schemas,
            parent_name=parent_name,
            config=config,
        )
        if isinstance(sub_prop, PropertyError):
            return PropertyError(detail=f"Invalid property in union {name}", data=sub_prop_data), schemas
        sub_properties.append(sub_prop)

    default = convert_chain((prop.get_base_type_string() for prop in sub_properties), data.default)
    return (
        UnionProperty(
            name=name,
            required=required,
            default=default,
            inner_properties=sub_properties,
            nullable=data.nullable,
            python_name=utils.PythonIdentifier(value=name, prefix=config.field_prefix),
            description=data.description,
            example=data.example,
        ),
        schemas,
    )
