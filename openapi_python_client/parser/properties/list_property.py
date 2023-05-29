from typing import Any, ClassVar, Generic, Set, Tuple, TypeVar, Union

import attr

from ... import schema as oai
from ... import utils
from ...config import Config
from ..errors import PropertyError
from .property import Property
from .schemas import ReferencePath, Schemas

InnerProp = TypeVar("InnerProp", bound=Property)


@attr.s(auto_attribs=True, frozen=True)
class ListProperty(Property, Generic[InnerProp]):
    """A property representing a list (array) of other properties"""

    inner_property: InnerProp
    template: ClassVar[str] = "list_property.py.jinja"

    # pylint: disable=unused-argument
    def get_base_type_string(self, *, quoted: bool = False) -> str:
        return f"List[{self.inner_property.get_type_string(quoted=not self.inner_property.is_base_type)}]"

    def get_base_json_type_string(self, *, quoted: bool = False) -> str:
        return f"List[{self.inner_property.get_type_string(json=True, quoted=not self.inner_property.is_base_type)}]"

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

    def get_lazy_imports(self, *, prefix: str) -> Set[str]:
        lazy_imports = super().get_lazy_imports(prefix=prefix)
        lazy_imports.update(self.inner_property.get_lazy_imports(prefix=prefix))
        return lazy_imports


def build_list_property(
    *,
    data: oai.Schema,
    name: str,
    required: bool,
    schemas: Schemas,
    parent_name: str,
    config: Config,
    process_properties: bool,
    roots: Set[Union[ReferencePath, utils.ClassName]],
) -> Tuple[Union[ListProperty[Any], PropertyError], Schemas]:
    """
    Build a ListProperty the right way, use this instead of the normal constructor.

    Args:
        data: `oai.Schema` representing this `ListProperty`.
        name: The name of this property where it's used.
        required: Whether or not this `ListProperty` can be `Unset` where it's used.
        schemas: Collected `Schemas` so far containing any classes or references.
        parent_name: The name of the thing containing this property (used for naming inner classes).
        config: User-provided config for overriding default behaviors.

    Returns:
        `(result, schemas)` where `schemas` is an updated version of the input named the same including any inner
        classes that were defined and `result` is either the `ListProperty` or a `PropertyError`.
    """
    if data.items is None:
        return PropertyError(data=data, detail="type array must have items defined"), schemas
    from .build import property_from_data  # TODO: Circular import

    inner_prop, schemas = property_from_data(
        name=f"{name}_item",
        required=True,
        data=data.items,
        schemas=schemas,
        parent_name=parent_name,
        config=config,
        process_properties=process_properties,
        roots=roots,
    )
    if isinstance(inner_prop, PropertyError):
        inner_prop.header = f'invalid data in items of array named "{name}"'
        return inner_prop, schemas
    return (
        ListProperty(
            name=name,
            required=required,
            default=None,
            inner_property=inner_prop,
            nullable=data.nullable,
            python_name=utils.PythonIdentifier(value=name, prefix=config.field_prefix),
            description=data.description,
            example=data.example,
        ),
        schemas,
    )
