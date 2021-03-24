__all__ = ["Class", "Schemas", "parse_reference_path"]

from typing import TYPE_CHECKING, Dict, List, NewType, Union, cast
from urllib.parse import urlparse

import attr
from pydantic import BaseModel

from ... import Config
from ... import schema as oai
from ... import utils
from ..errors import ParseError, PropertyError

if TYPE_CHECKING:  # pragma: no cover
    from .enum_property import EnumProperty
    from .model_property import ModelProperty
else:
    EnumProperty = "EnumProperty"
    ModelProperty = "ModelProperty"


_ReferencePath = NewType("_ReferencePath", str)
_ClassName = NewType("_ClassName", str)


def parse_reference_path(ref_path_raw: str) -> Union[_ReferencePath, ParseError]:
    parsed = urlparse(ref_path_raw)
    if parsed.scheme is not None or parsed.path is not None:
        return ParseError(detail="Remote references are not supported yet.")
    return cast(_ReferencePath, parsed.fragment)


class Class(BaseModel):
    """ Info about a generated class which will be in models """

    name: _ClassName
    module_name: str

    @staticmethod
    def from_string(*, string: str, config: Config) -> "Class":
        """ Get a Class from an arbitrary string """
        class_name = string.split("/")[-1]  # Get rid of ref path stuff
        class_name = utils.pascal_case(class_name)

        if class_name in config.class_overrides:
            return config.class_overrides[class_name]

        return Class(name=cast(_ClassName, class_name), module_name=utils.snake_case(class_name))


@attr.s(auto_attribs=True, frozen=True)
class Schemas:
    """ Structure for containing all defined, shareable, and reusable schemas (attr classes and Enums) """

    classes_by_reference: Dict[_ReferencePath, Union[EnumProperty, ModelProperty]] = attr.ib(factory=dict)
    classes_by_name: Dict[_ClassName, Union[EnumProperty, ModelProperty]] = attr.ib(factory=dict)
    errors: List[ParseError] = attr.ib(factory=list)


def update_schemas_with_data(
    ref_path: _ReferencePath, data: oai.Schema, schemas: Schemas
) -> Union[Schemas, PropertyError]:
    from . import build_enum_property, build_model_property

    prop: Union[PropertyError, ModelProperty, EnumProperty]
    if data.enum is not None:
        prop, schemas = build_enum_property(
            data=data, name=ref_path, required=True, schemas=schemas, enum=data.enum, parent_name=None
        )
    else:
        prop, schemas = build_model_property(data=data, name=ref_path, schemas=schemas, required=True, parent_name=None)
    if isinstance(prop, PropertyError):
        return prop
    schemas = attr.evolve(schemas, classes_by_reference={ref_path: prop, **schemas.classes_by_reference})
    return schemas
