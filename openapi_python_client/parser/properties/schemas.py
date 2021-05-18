__all__ = ["Class", "Schemas", "parse_reference_path", "update_schemas_with", "_ReferencePath"]

from typing import TYPE_CHECKING, Dict, Generic, List, NewType, Optional, Set, Tuple, TypeVar, Union, cast
from urllib.parse import urlparse

import attr

from ... import Config
from ... import schema as oai
from ... import utils
from ..errors import ParseError, PropertyError, RecursiveReferenceInterupt

if TYPE_CHECKING:  # pragma: no cover
    from .enum_property import EnumProperty
    from .model_property import ModelProperty
else:
    EnumProperty = "EnumProperty"
    ModelProperty = "ModelProperty"

T = TypeVar("T")
_ReferencePath = NewType("_ReferencePath", str)
_ClassName = NewType("_ClassName", str)


def parse_reference_path(ref_path_raw: str) -> Union[_ReferencePath, ParseError]:
    parsed = urlparse(ref_path_raw)
    if parsed.scheme or parsed.path:
        return ParseError(detail=f"Remote references such as {ref_path_raw} are not supported yet.")
    return cast(_ReferencePath, parsed.fragment)


@attr.s(auto_attribs=True)
class _Holder(Generic[T]):
    data: Optional[T]


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

    classes_by_reference: Dict[
        _ReferencePath, _Holder[Union[EnumProperty, ModelProperty, RecursiveReferenceInterupt]]
    ] = attr.ib(factory=dict)
    classes_by_name: Dict[
        _ClassName, _Holder[Union[EnumProperty, ModelProperty, RecursiveReferenceInterupt]]
    ] = attr.ib(factory=dict)
    errors: List[ParseError] = attr.ib(factory=list)


def update_schemas_with(
    *,
    ref_path: _ReferencePath,
    data: Union[oai.Reference, oai.Schema],
    schemas: Schemas,
    visited: Tuple[_ReferencePath, Set[_ReferencePath]],
    config: Config,
) -> Union[Schemas, PropertyError]:
    if isinstance(data, oai.Reference):
        return _update_schemas_with_reference(
            ref_path=ref_path, data=data, schemas=schemas, visited=visited, config=config
        )
    else:
        return _update_schemas_with_data(ref_path=ref_path, data=data, schemas=schemas, visited=visited, config=config)


def _update_schemas_with_reference(
    *, ref_path: _ReferencePath, data: oai.Reference, schemas: Schemas, visited: Tuple[_ReferencePath, Set[_ReferencePath]], config: Config
) -> Union[Schemas, PropertyError]:
    reference_pointer = parse_reference_path(data.ref)
    if isinstance(reference_pointer, ParseError):
        return PropertyError(detail=reference_pointer.detail, data=data)

    curr, previous = visited
    previous.add(reference_pointer)
    resolved_reference = schemas.classes_by_reference.get(reference_pointer)
    if resolved_reference:
        return attr.evolve(schemas, classes_by_reference={ref_path: resolved_reference, **schemas.classes_by_reference})
    else:
        return PropertyError(f"Reference {ref_path} could not be resolved", data=data)


def _update_schemas_with_data(
    *, ref_path: _ReferencePath, data: oai.Schema, schemas: Schemas, visited: Tuple[_ReferencePath, Set[_ReferencePath]], config: Config
) -> Union[Schemas, PropertyError]:
    from . import build_enum_property, build_model_property

    prop: Union[PropertyError, ModelProperty, EnumProperty]
    if data.enum is not None:
        prop, schemas = build_enum_property(
            data=data, name=ref_path, required=True, schemas=schemas, enum=data.enum, parent_name=None, config=config
        )
    else:
        prop, schemas = build_model_property(
            data=data, name=ref_path, schemas=schemas, required=True, parent_name=None, config=config
        )

    holder = schemas.classes_by_reference.get(ref_path)
    if isinstance(prop, PropertyError):
        curr, previous = visited
        if (ref_path in previous or curr in f"{prop.data}") and not holder:
            holder = _Holder(data=RecursiveReferenceInterupt())
            schemas = attr.evolve(schemas, classes_by_reference={ref_path: holder, **schemas.classes_by_reference})
            return RecursiveReferenceInterupt(schemas=schemas)
        return prop

    if holder:
        holder.data = prop
    else:
        schemas = attr.evolve(
            schemas, classes_by_reference={ref_path: _Holder(data=prop), **schemas.classes_by_reference}
        )
    return schemas
