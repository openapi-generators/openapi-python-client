__all__ = ["Class", "Schemas", "parse_reference_path", "update_schemas_with_data"]

from typing import TYPE_CHECKING, Dict, List, NewType, Union, cast
from urllib.parse import urlparse

import attr

from ... import Config
from ... import schema as oai
from ... import utils
from ..errors import ParseError, PropertyError

if TYPE_CHECKING:  # pragma: no cover
    from .property import Property
else:
    Property = "Property"


_ReferencePath = NewType("_ReferencePath", str)
_ClassName = NewType("_ClassName", str)


def parse_reference_path(ref_path_raw: str) -> Union[_ReferencePath, ParseError]:
    parsed = urlparse(ref_path_raw)
    if parsed.scheme or parsed.path:
        return ParseError(detail=f"Remote references such as {ref_path_raw} are not supported yet.")
    return cast(_ReferencePath, parsed.fragment)


@attr.s(auto_attribs=True, frozen=True)
class Class:
    """Represents Python class which will be generated from an OpenAPI schema"""

    name: _ClassName
    module_name: str

    @staticmethod
    def from_string(*, string: str, config: Config) -> "Class":
        """Get a Class from an arbitrary string"""
        class_name = string.split("/")[-1]  # Get rid of ref path stuff
        class_name = utils.pascal_case(class_name)
        override = config.class_overrides.get(class_name)

        if override is not None and override.class_name is not None:
            class_name = override.class_name

        if override is not None and override.module_name is not None:
            module_name = override.module_name
        else:
            module_name = utils.snake_case(class_name)

        return Class(name=cast(_ClassName, class_name), module_name=module_name)


@attr.s(auto_attribs=True, frozen=True)
class Schemas:
    """Structure for containing all defined, shareable, and reusable schemas (attr classes and Enums)"""

    classes_by_reference: Dict[_ReferencePath, Property] = attr.ib(factory=dict)
    classes_by_name: Dict[_ClassName, Property] = attr.ib(factory=dict)
    errors: List[ParseError] = attr.ib(factory=list)


def update_schemas_with_data(
    *, ref_path: _ReferencePath, data: oai.Schema, schemas: Schemas, config: Config
) -> Union[Schemas, PropertyError]:
    from . import property_from_data

    prop: Union[PropertyError, Property]
    prop, schemas = property_from_data(
        data=data, name=ref_path, schemas=schemas, required=True, parent_name="", config=config
    )

    if isinstance(prop, PropertyError):
        return prop

    schemas = attr.evolve(schemas, classes_by_reference={ref_path: prop, **schemas.classes_by_reference})
    return schemas
