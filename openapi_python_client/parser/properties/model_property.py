from itertools import chain
from typing import ClassVar, Dict, List, NamedTuple, Optional, Set, Tuple, Union

import attr

from ... import Config
from ... import schema as oai
from ... import utils
from ..errors import ParseError, PropertyError
from .property import Property
from .schemas import Class, Schemas, parse_reference_path


@attr.s(auto_attribs=True, frozen=True)
class ModelProperty(Property):
    """A property which refers to another Schema"""

    class_info: Class
    required_properties: List[Property]
    optional_properties: List[Property]
    description: str
    relative_imports: Set[str]
    additional_properties: Union[bool, Property]
    _json_type_string: ClassVar[str] = "Dict[str, Any]"

    template: ClassVar[str] = "model_property.py.jinja"
    json_is_dict: ClassVar[bool] = True

    def get_base_type_string(self, json: bool = False) -> str:
        return self.class_info.name

    def get_imports(self, *, prefix: str) -> Set[str]:
        """
        Get a set of import strings that should be included when this property is used somewhere

        Args:
            prefix: A prefix to put before any relative (local) module names. This should be the number of . to get
            back to the root of the generated client.
        """
        imports = super().get_imports(prefix=prefix)
        imports.update(
            {
                f"from {prefix}models.{self.class_info.module_name} import {self.class_info.name}",
                "from typing import Dict",
                "from typing import cast",
            }
        )
        return imports


def _merge_properties(first: Property, second: Property) -> Union[Property, PropertyError]:
    if first.__class__ != second.__class__:
        return PropertyError(header="Cannot merge properties", detail="Properties are two different types")
    nullable = first.nullable and second.nullable
    required = first.required or second.required
    first = attr.evolve(first, nullable=nullable, required=required)
    second = attr.evolve(second, nullable=nullable, required=required)
    if first != second:
        return PropertyError(header="Cannot merge properties", detail="Properties has conflicting values")
    return first


class _PropertyData(NamedTuple):
    optional_props: List[Property]
    required_props: List[Property]
    relative_imports: Set[str]
    schemas: Schemas


def _process_properties(
    *, data: oai.Schema, schemas: Schemas, class_name: str, config: Config
) -> Union[_PropertyData, PropertyError]:
    from . import property_from_data

    properties: Dict[str, Property] = {}
    relative_imports: Set[str] = set()
    required_set = set(data.required or [])

    def _check_existing(prop: Property) -> Union[Property, PropertyError]:
        nonlocal properties

        existing = properties.get(prop.name)
        prop_or_error = _merge_properties(existing, prop) if existing else prop
        if isinstance(prop_or_error, PropertyError):
            prop_or_error.header = f"Found conflicting properties named {prop.name} when creating {class_name}"
            return prop_or_error
        properties[prop_or_error.name] = prop_or_error
        return prop_or_error

    unprocessed_props = data.properties or {}
    for sub_prop in data.allOf or []:
        if isinstance(sub_prop, oai.Reference):
            ref_path = parse_reference_path(sub_prop.ref)
            if isinstance(ref_path, ParseError):
                return PropertyError(detail=ref_path.detail, data=sub_prop)
            sub_model = schemas.classes_by_reference.get(ref_path)
            if sub_model is None:
                return PropertyError(f"Reference {sub_prop.ref} not found")
            if not isinstance(sub_model, ModelProperty):
                return PropertyError("Cannot take allOf a non-object")
            for prop in chain(sub_model.required_properties, sub_model.optional_properties):
                prop_or_error = _check_existing(prop)
                if isinstance(prop_or_error, PropertyError):
                    return prop_or_error
        else:
            unprocessed_props.update(sub_prop.properties or {})
            required_set.update(sub_prop.required or [])

    for key, value in unprocessed_props.items():
        prop_required = key in required_set
        prop_or_error, schemas = property_from_data(
            name=key, required=prop_required, data=value, schemas=schemas, parent_name=class_name, config=config
        )
        if isinstance(prop_or_error, Property):
            prop_or_error = _check_existing(prop_or_error)
        if isinstance(prop_or_error, PropertyError):
            return prop_or_error

        properties[prop_or_error.name] = prop_or_error

    required_properties = []
    optional_properties = []
    for prop in properties.values():
        if prop.required and not prop.nullable:
            required_properties.append(prop)
        else:
            optional_properties.append(prop)
        relative_imports.update(prop.get_imports(prefix=".."))

    return _PropertyData(
        optional_props=optional_properties,
        required_props=required_properties,
        relative_imports=relative_imports,
        schemas=schemas,
    )


def _get_additional_properties(
    *,
    schema_additional: Union[None, bool, oai.Reference, oai.Schema],
    schemas: Schemas,
    class_name: str,
    config: Config,
) -> Tuple[Union[bool, Property, PropertyError], Schemas]:
    from . import property_from_data

    if schema_additional is None:
        return True, schemas

    if isinstance(schema_additional, bool):
        return schema_additional, schemas

    if isinstance(schema_additional, oai.Schema) and not any(schema_additional.dict().values()):
        # An empty schema
        return True, schemas

    additional_properties, schemas = property_from_data(
        name="AdditionalProperty",
        required=True,  # in the sense that if present in the dict will not be None
        data=schema_additional,
        schemas=schemas,
        parent_name=class_name,
        config=config,
    )
    return additional_properties, schemas


def build_model_property(
    *, data: oai.Schema, name: str, schemas: Schemas, required: bool, parent_name: Optional[str], config: Config
) -> Tuple[Union[ModelProperty, PropertyError], Schemas]:
    """
    A single ModelProperty from its OAI data

    Args:
        data: Data of a single Schema
        name: Name by which the schema is referenced, such as a model name.
            Used to infer the type name if a `title` property is not available.
        schemas: Existing Schemas which have already been processed (to check name conflicts)
        required: Whether or not this property is required by the parent (affects typing)
        parent_name: The name of the property that this property is inside of (affects class naming)
        config: Config data for this run of the generator, used to modifying names
    """
    class_string = data.title or name
    if parent_name:
        class_string = f"{utils.pascal_case(parent_name)}{utils.pascal_case(class_string)}"
    class_info = Class.from_string(string=class_string, config=config)

    property_data = _process_properties(data=data, schemas=schemas, class_name=class_info.name, config=config)
    if isinstance(property_data, PropertyError):
        return property_data, schemas
    schemas = property_data.schemas

    additional_properties, schemas = _get_additional_properties(
        schema_additional=data.additionalProperties, schemas=schemas, class_name=class_info.name, config=config
    )
    if isinstance(additional_properties, Property):
        property_data.relative_imports.update(additional_properties.get_imports(prefix=".."))
    elif isinstance(additional_properties, PropertyError):
        return additional_properties, schemas

    prop = ModelProperty(
        class_info=class_info,
        required_properties=property_data.required_props,
        optional_properties=property_data.optional_props,
        relative_imports=property_data.relative_imports,
        description=data.description or "",
        default=None,
        nullable=data.nullable,
        required=required,
        name=name,
        additional_properties=additional_properties,
    )
    if class_info.name in schemas.classes_by_name:
        error = PropertyError(data=data, detail=f'Attempted to generate duplicate models with name "{class_info.name}"')
        return error, schemas

    schemas = attr.evolve(schemas, classes_by_name={**schemas.classes_by_name, class_info.name: prop})
    return prop, schemas
