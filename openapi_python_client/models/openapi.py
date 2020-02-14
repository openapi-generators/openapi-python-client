from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set

import stringcase

from .properties import Property, property_from_dict, DateTimeProperty, ListProperty, RefProperty, EnumProperty


class Method(Enum):
    """ HTTP Methods """
    GET = "get"
    POST = "post"
    PATCH = "patch"


class ParameterLocation(Enum):
    """ The places Parameters can be put when calling an Endpoint """
    QUERY = "query"
    PATH = "path"


@dataclass
class Parameter:
    """ A parameter in an Endpoint """
    location: ParameterLocation
    property: Property

    @staticmethod
    def from_dict(d: Dict, /) -> Parameter:
        """ Construct a parameter from it's OpenAPI dict form """
        return Parameter(
            location=ParameterLocation(d["in"]),
            property=property_from_dict(
                name=d["name"],
                required=d["required"],
                data=d["schema"],
            ),
        )


@dataclass
class Endpoint:
    """
    Describes a single endpoint on the server
    """
    path: str
    method: Method
    description: Optional[str]
    name: str
    parameters: List[Parameter]
    tag: Optional[str] = None

    @staticmethod
    def get_list_from_dict(d: Dict[str, Dict[str, Dict]], /) -> List[Endpoint]:
        """ Parse the openapi paths data to get a list of endpoints """
        endpoints = []
        for path, path_data in d.items():
            for method, method_data in path_data.items():
                parameters: List[Parameter] = []
                for param_dict in method_data.get("parameters", []):
                    parameters.append(Parameter.from_dict(param_dict))
                endpoint = Endpoint(
                    path=path,
                    method=Method(method),
                    description=method_data.get("description"),
                    name=method_data["operationId"],
                    parameters=parameters,
                    tag=method_data.get("tags", [None])[0],
                )
                endpoints.append(endpoint)
        return endpoints


@dataclass
class Schema:
    """
    Describes a schema, AKA data model used in requests.

    These will all be converted to dataclasses in the client
    """

    title: str
    properties: List[Property]
    description: str
    relative_imports: Set[str] = field(default_factory=set)

    @staticmethod
    def from_dict(d: Dict, /) -> Schema:
        """ A single Schema from its dict representation """
        required = set(d.get("required", []))
        properties: List[Property] = []
        schema = Schema(title=d["title"], properties=properties, description=d.get("description", ""))
        for key, value in d["properties"].items():
            p = property_from_dict(name=key, required=key in required, data=value)
            properties.append(p)
            if isinstance(p, (ListProperty, RefProperty)) and p.ref:
                schema.relative_imports.add(f"from .{stringcase.snakecase(p.ref)} import {p.ref}")
        return schema

    @staticmethod
    def dict(d: Dict, /) -> Dict[str, Schema]:
        """ Get a list of Schemas from an OpenAPI dict """
        result = {}
        for data in d.values():
            s = Schema.from_dict(data)
            result[s.title] = s
        return result


@dataclass
class OpenAPI:
    """ Top level OpenAPI spec """

    title: str
    description: str
    version: str
    security_schemes: Dict
    schemas: Dict[str, Schema]
    endpoints: List[Endpoint]
    enums: Dict[str, List[str]]

    @staticmethod
    def from_dict(d: Dict, /) -> OpenAPI:
        """ Create an OpenAPI from dict """
        schemas = Schema.dict(d["components"]["schemas"])
        enums = {}
        for schema in schemas.values():
            for prop in schema.properties:
                if isinstance(prop, EnumProperty):
                    enum_class_name = stringcase.pascalcase(prop.name)
                    enums[enum_class_name] = prop.values
                    schema.relative_imports.add(f"from .{prop.name} import {enum_class_name}")

        return OpenAPI(
            title=d["info"]["title"],
            description=d["info"]["description"],
            version=d["info"]["version"],
            endpoints=Endpoint.get_list_from_dict(d["paths"]),
            schemas=schemas,
            security_schemes=d["components"]["securitySchemes"],
            enums=enums,
        )
