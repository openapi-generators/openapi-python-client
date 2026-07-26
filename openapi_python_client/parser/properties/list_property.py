from __future__ import annotations

from typing import Any, ClassVar

from attr import define, field

from ... import Config, strings
from ... import schema as oai
from ..errors import PropertyError
from .protocol import PropertyProtocol, Value, convert_example
from .schemas import ReferencePath, Schemas


@define
class ListProperty(PropertyProtocol):
    """A property representing a list (array) of other properties"""

    name: oai.UntrustedString
    required: bool
    default: Value | None
    python_name: strings.PythonIdentifier
    description: oai.UntrustedString | None
    example: oai.UntrustedString | None = field(converter=convert_example)
    inner_property: PropertyProtocol
    template: ClassVar[str] = "list_property.py.jinja"

    @classmethod
    def build(
        cls,
        *,
        data: oai.Schema,
        name: oai.UntrustedString,
        required: bool,
        schemas: Schemas,
        parent_name: str,
        config: Config,
        process_properties: bool,
        roots: set[ReferencePath | strings.ClassName],
    ) -> tuple[ListProperty | PropertyError, Schemas]:
        """
        Build a ListProperty the right way, use this instead of the normal constructor.

        Args:
            data: `oai.Schema` representing this `ListProperty`.
            name: The name of this property where it's used.
            required: Whether this `ListProperty` can be `Unset` where it's used.
            schemas: Collected `Schemas` so far containing any classes or references.
            parent_name: The name of the thing containing this property (used for naming inner classes).
            config: User-provided config for overriding default behaviors.
            process_properties: If the new property is a ModelProperty, determines whether it will be initialized with
                property data
            roots: The set of `ReferencePath`s and `ClassName`s to remove from the schemas if a child reference becomes
                invalid

        Returns:
            `(result, schemas)` where `schemas` is an updated version of the input named the same including any inner
            classes that were defined and `result` is either the `ListProperty` or a `PropertyError`.
        """
        from . import property_from_data  # noqa: PLC0415

        if data.items is None and not data.prefixItems:
            return (
                PropertyError(
                    data=data,
                    detail="type array must have items or prefixItems defined",
                ),
                schemas,
            )

        items = data.prefixItems or []
        if data.items:
            items.append(data.items)

        if len(items) == 1:
            inner_schema = items[0]
        else:
            inner_schema = oai.Schema(anyOf=items)

        inner_prop, schemas = property_from_data(
            name=oai.UntrustedString(f"{name.get_untrusted_value()}_item"),
            required=True,
            data=inner_schema,
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
                python_name=strings.PythonIdentifier(value=name, prefix=config.field_prefix),
                description=data.description,
                example=data.example,
            ),
            schemas,
        )

    def convert_value(self, value: Any) -> Value | PropertyError | None:
        return None  # pragma: no cover

    def get_base_type_string(self) -> strings.PythonCode:
        return strings.PythonCode(f"list[{self.inner_property.get_type_string().as_unembedded_code()}]")

    def get_base_json_type_string(self) -> strings.PythonCode:
        return strings.PythonCode(f"list[{self.inner_property.get_type_string(json=True).as_unembedded_code()}]")

    def get_instance_type_string(self) -> strings.PythonCode:
        """Get a code representation of runtime type that should be used for `isinstance` checks"""
        return strings.PythonCode("list")

    def get_imports(self, *, prefix: str) -> set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names. This should be the number of . to get
            back to the root of the generated client.
        """
        imports = super().get_imports(prefix=prefix)
        imports.update(self.inner_property.get_imports(prefix=prefix))
        imports.add("from typing import cast")
        return imports

    def get_lazy_imports(self, *, prefix: str) -> set[str]:
        lazy_imports = super().get_lazy_imports(prefix=prefix)
        lazy_imports.update(self.inner_property.get_lazy_imports(prefix=prefix))
        return lazy_imports

    def get_type_string(
        self,
        no_optional: bool = False,
        json: bool = False,
    ) -> strings.PythonCode:
        """
        Get a Python code representation of type that should be used when declaring this property

        Args:
            no_optional: Do not include Optional or Unset even if the value is optional (needed for isinstance checks)
            json: True if the type refers to the property after JSON serialization
        """
        if json:
            type_string = self.get_base_json_type_string()
        else:
            type_string = self.get_base_type_string()

        if no_optional or self.required:
            return type_string
        return strings.PythonCode(f"{type_string.as_unembedded_code()} | Unset")
