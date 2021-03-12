from typing import ClassVar, List, NamedTuple, Optional, Set, Tuple, Union

import attr

from ... import schema as oai
from ... import utils
from ..errors import PropertyError
from ..reference import Reference
from .property import Property
from .schemas import Schemas


@attr.s(auto_attribs=True, frozen=True)
class ModelProperty(Property):
    """ A property which refers to another Schema """

    reference: Reference
    required_properties: List[Property]
    optional_properties: List[Property]
    description: str
    relative_imports: Set[str]
    additional_properties: Union[bool, Property]

    template: ClassVar[str] = "model_property.py.jinja"
    json_is_dict: ClassVar[bool] = True

    def get_type_string(self, no_optional: bool = False) -> str:
        """ Get a string representation of type that should be used when declaring this property """
        type_string = self.reference.class_name
        if no_optional:
            return type_string
        if self.nullable:
            type_string = f"Optional[{type_string}]"
        if not self.required:
            type_string = f"Union[{type_string}, Unset]"
        return type_string

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
                f"from {prefix}models.{self.reference.module_name} import {self.reference.class_name}",
                "from typing import Dict",
                "from typing import cast",
            }
        )
        return imports


class _PropertyData(NamedTuple):
    optional_props: List[Property]
    required_props: List[Property]
    relative_imports: Set[str]
    schemas: Schemas


def _process_properties(*, data: oai.Schema, schemas: Schemas, class_name: str) -> Union[_PropertyData, PropertyError]:
    from . import property_from_data

    required_properties: List[Property] = []
    optional_properties: List[Property] = []
    relative_imports: Set[str] = set()
    required_set = set(data.required or [])

    all_props = data.properties or {}
    for sub_prop in data.allOf or []:
        if isinstance(sub_prop, oai.Reference):
            source_name = Reference.from_ref(sub_prop.ref).class_name
            sub_model = schemas.models.get(source_name)
            if sub_model is None:
                return PropertyError(f"Reference {sub_prop.ref} not found")
            required_properties.extend(sub_model.required_properties)
            optional_properties.extend(sub_model.optional_properties)
            relative_imports.update(sub_model.relative_imports)
        else:
            all_props.update(sub_prop.properties or {})
            required_set.update(sub_prop.required or [])

    for key, value in all_props.items():
        prop_required = key in required_set
        prop, schemas = property_from_data(
            name=key, required=prop_required, data=value, schemas=schemas, parent_name=class_name
        )
        if isinstance(prop, PropertyError):
            return prop
        if prop_required and not prop.nullable:
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


def build_model_property(
    *, data: oai.Schema, name: str, schemas: Schemas, required: bool, parent_name: Optional[str]
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
    """
    from . import property_from_data

    class_name = data.title or name
    if parent_name:
        class_name = f"{utils.pascal_case(parent_name)}{utils.pascal_case(class_name)}"
    ref = Reference.from_ref(class_name)

    property_data = _process_properties(data=data, schemas=schemas, class_name=class_name)
    if isinstance(property_data, PropertyError):
        return property_data, schemas
    schemas = property_data.schemas

    additional_properties: Union[bool, Property, PropertyError]
    if data.additionalProperties is None:
        additional_properties = True
    elif isinstance(data.additionalProperties, bool):
        additional_properties = data.additionalProperties
    elif isinstance(data.additionalProperties, oai.Schema) and not any(data.additionalProperties.dict().values()):
        # An empty schema
        additional_properties = True
    else:
        assert isinstance(data.additionalProperties, (oai.Schema, oai.Reference))
        additional_properties, schemas = property_from_data(
            name="AdditionalProperty",
            required=True,  # in the sense that if present in the dict will not be None
            data=data.additionalProperties,
            schemas=schemas,
            parent_name=class_name,
        )
        if isinstance(additional_properties, PropertyError):
            return additional_properties, schemas
        property_data.relative_imports.update(additional_properties.get_imports(prefix=".."))

    prop = ModelProperty(
        reference=ref,
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
    if prop.reference.class_name in schemas.models:
        error = PropertyError(
            data=data, detail=f'Attempted to generate duplicate models with name "{prop.reference.class_name}"'
        )
        return error, schemas

    schemas = attr.evolve(schemas, models={**schemas.models, prop.reference.class_name: prop})
    return prop, schemas
