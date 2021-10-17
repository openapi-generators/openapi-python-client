__all__ = ["Class", "Schemas", "parse_reference_path", "update_schemas_with_data"]

from typing import TYPE_CHECKING, Dict, List, NewType, Union, cast
from urllib.parse import urlparse

import attr

from ... import Config
from ... import schema as oai
from ...utils import ClassName, PythonIdentifier
from ..errors import ParseError, PropertyError

if TYPE_CHECKING:  # pragma: no cover
    from .property import Property
else:
    Property = "Property"  # pylint: disable=invalid-name


_ReferencePath = NewType("_ReferencePath", str)


def parse_reference_path(ref_path_raw: str) -> Union[_ReferencePath, ParseError]:
    """
    Takes a raw string provided in a `$ref` and turns it into a validated `_ReferencePath` or a `ParseError` if
    validation fails.

    See Also:
        - https://swagger.io/docs/specification/using-ref/
    """
    parsed = urlparse(ref_path_raw)
    if parsed.scheme or parsed.path:
        return ParseError(detail=f"Remote references such as {ref_path_raw} are not supported yet.")
    return cast(_ReferencePath, parsed.fragment)


@attr.s(auto_attribs=True, frozen=True)
class Class:
    """Represents Python class which will be generated from an OpenAPI schema"""

    name: ClassName
    module_name: PythonIdentifier

    @staticmethod
    def from_string(*, string: str, config: Config) -> "Class":
        """Get a Class from an arbitrary string"""
        class_name = string.split("/")[-1]  # Get rid of ref path stuff
        class_name = ClassName(class_name, config.field_prefix)
        override = config.class_overrides.get(class_name)

        if override is not None and override.class_name is not None:
            class_name = ClassName(override.class_name, config.field_prefix)

        if override is not None and override.module_name is not None:
            module_name = override.module_name
        else:
            module_name = class_name
        module_name = PythonIdentifier(module_name, config.field_prefix)

        return Class(name=class_name, module_name=module_name)


@attr.s(auto_attribs=True, frozen=True)
class Schemas:
    """Structure for containing all defined, shareable, and reusable schemas (attr classes and Enums)"""

    classes_by_reference: Dict[_ReferencePath, Property] = attr.ib(factory=dict)
    classes_by_name: Dict[ClassName, Property] = attr.ib(factory=dict)
    errors: List[ParseError] = attr.ib(factory=list)


def update_schemas_with_data(
    *, ref_path: _ReferencePath, data: oai.Schema, schemas: Schemas, config: Config
) -> Union[Schemas, PropertyError]:
    """
    Update a `Schemas` using some new reference.

    Args:
        ref_path: The output of `parse_reference_path` (validated $ref).
        data: The schema of the thing to add to Schemas.
        schemas: `Schemas` up until now.
        config: User-provided config for overriding default behavior.

    Returns:
        Either the updated `schemas` input or a `PropertyError` if something went wrong.

    See Also:
        - https://swagger.io/docs/specification/using-ref/
    """
    from . import property_from_data

    prop: Union[PropertyError, Property]
    prop, schemas = property_from_data(
        data=data, name=ref_path, schemas=schemas, required=True, parent_name="", config=config
    )

    if isinstance(prop, PropertyError):
        prop.detail = f"{prop.header}: {prop.detail}"
        prop.header = f"Unable to parse schema {ref_path}"
        if isinstance(prop.data, oai.Reference) and prop.data.ref.endswith(ref_path):  # pragma: nocover
            prop.detail += (
                "\n\nRecursive and circular references are not supported. "
                "See https://github.com/openapi-generators/openapi-python-client/issues/466"
            )
        return prop

    schemas = attr.evolve(schemas, classes_by_reference={ref_path: prop, **schemas.classes_by_reference})
    return schemas
