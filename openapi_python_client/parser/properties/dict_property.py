from __future__ import annotations

from typing import Any, ClassVar

from attr import define

from ... import Config, utils
from ... import schema as oai
from ..errors import PropertyError
from .protocol import PropertyProtocol, Value
from .schemas import ReferencePath, Schemas


@define
class DictProperty(PropertyProtocol):
    """A property representing a dict (map) with string keys and typed values.

    Generated from an OpenAPI schema with ``additionalProperties`` and no
    ``properties``/``allOf``, so the underlying Python type is ``dict[str, T]``
    instead of an empty model class.
    """

    name: str
    required: bool
    default: Value | None
    python_name: utils.PythonIdentifier
    description: str | None
    example: str | None
    inner_property: PropertyProtocol
    template: ClassVar[str] = "dict_property.py.jinja"

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
        process_properties: bool,
        roots: set[ReferencePath | utils.ClassName],
    ) -> tuple[DictProperty | PropertyError, Schemas]:
        from . import property_from_data  # noqa: PLC0415

        additional = data.additionalProperties
        if additional is None or isinstance(additional, bool):
            return (
                PropertyError(
                    data=data,
                    detail="DictProperty requires a typed additionalProperties schema",
                ),
                schemas,
            )

        inner_prop, schemas = property_from_data(
            name=f"{name}_item",
            required=True,
            data=additional,
            schemas=schemas,
            parent_name=parent_name,
            config=config,
            process_properties=process_properties,
            roots=roots,
        )
        if isinstance(inner_prop, PropertyError):
            inner_prop.header = f'invalid data in additionalProperties of dict named "{name}"'
            return inner_prop, schemas

        return (
            cls(
                name=name,
                required=required,
                default=None,
                inner_property=inner_prop,
                python_name=utils.PythonIdentifier(value=name, prefix=config.field_prefix),
                description=data.description,
                example=data.example,
            ),
            schemas,
        )

    def convert_value(self, value: Any) -> Value | None | PropertyError:
        return None  # pragma: no cover

    def get_base_type_string(self) -> str:
        return f"dict[str, {self.inner_property.get_type_string()}]"

    def get_base_json_type_string(self) -> str:
        return f"dict[str, {self.inner_property.get_type_string(json=True)}]"

    def get_instance_type_string(self) -> str:
        return "dict"

    def get_imports(self, *, prefix: str) -> set[str]:
        imports = super().get_imports(prefix=prefix)
        imports.update(self.inner_property.get_imports(prefix=prefix))
        return imports

    def get_lazy_imports(self, *, prefix: str) -> set[str]:
        lazy_imports = super().get_lazy_imports(prefix=prefix)
        lazy_imports.update(self.inner_property.get_lazy_imports(prefix=prefix))
        return lazy_imports

    def get_type_string(
        self,
        no_optional: bool = False,
        json: bool = False,
    ) -> str:
        if json:
            type_string = self.get_base_json_type_string()
        else:
            type_string = self.get_base_type_string()

        if no_optional or self.required:
            return type_string
        return f"{type_string} | Unset"
