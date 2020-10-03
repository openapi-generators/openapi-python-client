""" A Model is used to generate classes from schemas. This module contains Model and helper functions for it """
from dataclasses import dataclass
from typing import List, Set, Union

from .. import schema as oai
from .errors import ParseError
from .properties import Property, property_from_data
from .reference import Reference


@dataclass
class Model:
    """
    A data model used by the API- usually a Schema with type "object".

    These will all be converted to dataclasses in the client
    """

    reference: Reference
    required_properties: List[Property]
    optional_properties: List[Property]
    description: str
    relative_imports: Set[str]


def model_from_data(*, data: oai.Schema, name: str) -> Union["Model", ParseError]:
    """A single Model from its OAI data

    Args:
        data: Data of a single Schema
        name: Name by which the schema is referenced, such as a model name.
            Used to infer the type name if a `title` property is not available.
    """
    required_set = set(data.required or [])
    required_properties: List[Property] = []
    optional_properties: List[Property] = []
    relative_imports: Set[str] = set()

    ref = Reference.from_ref(data.title or name)

    for key, value in (data.properties or {}).items():
        required = key in required_set
        p = property_from_data(name=key, required=required, data=value)
        if isinstance(p, ParseError):
            return p
        if required:
            required_properties.append(p)
        else:
            optional_properties.append(p)
        relative_imports.update(p.get_imports(prefix=".."))

    model = Model(
        reference=ref,
        required_properties=required_properties,
        optional_properties=optional_properties,
        relative_imports=relative_imports,
        description=data.description or "",
    )
    return model
