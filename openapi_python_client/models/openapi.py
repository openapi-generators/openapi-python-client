from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set

import stringcase

from .properties import Property, property_from_dict, ListProperty, RefProperty, EnumProperty
from .responses import Response, response_from_dict


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
            property=property_from_dict(name=d["name"], required=d["required"], data=d["schema"],),
        )


def _import_string_from_ref(ref: str, prefix: str = "") -> str:
    return f"from {prefix}.{stringcase.snakecase(ref)} import {ref}"


@dataclass
class EndpointCollection:
    """ A bunch of endpoints grouped under a tag that will become a module """
    tag: str
    endpoints: List[Endpoint] = field(default_factory=list)
    relative_imports: Set[str] = field(default_factory=set)

    @staticmethod
    def from_dict(d: Dict[str, Dict[str, Dict]], /) -> Dict[str, EndpointCollection]:
        """ Parse the openapi paths data to get EndpointCollections by tag """
        endpoints_by_tag: Dict[str, EndpointCollection] = {}
        for path, path_data in d.items():
            for method, method_data in path_data.items():
                parameters: List[Parameter] = []
                responses: List[Response] = []
                for param_dict in method_data.get("parameters", []):
                    parameters.append(Parameter.from_dict(param_dict))
                tag = method_data.get("tags", ["default"])[0]
                for code, response_dict in method_data["responses"].items():
                    response = response_from_dict(
                        status_code=int(code),
                        data=response_dict,
                    )
                    responses.append(response)
                form_body_ref = None
                if "requestBody" in method_data:
                    form_body_ref = Endpoint.parse_request_body(method_data["requestBody"])

                endpoint = Endpoint(
                    path=path,
                    method=method,
                    description=method_data.get("description"),
                    name=method_data["operationId"],
                    parameters=parameters,
                    responses=responses,
                    form_body_ref=form_body_ref,
                )

                collection = endpoints_by_tag.setdefault(tag, EndpointCollection(tag=tag))
                collection.endpoints.append(endpoint)
                if form_body_ref:
                    collection.relative_imports.add(_import_string_from_ref(form_body_ref, prefix="..models"))
        return endpoints_by_tag


@dataclass
class Endpoint:
    """
    Describes a single endpoint on the server
    """

    path: str
    method: str
    description: Optional[str]
    name: str
    parameters: List[Parameter]
    responses: List[Response]
    form_body_ref: Optional[str]

    @staticmethod
    def parse_request_body(body: Dict, /) -> Optional[str]:
        """ Return form_body_ref """
        form_body_ref = None
        body_content = body["content"]
        form_body = body_content.get("application/x-www-form-urlencoded")
        if form_body:
            form_body_ref = form_body["schema"]["$ref"].split("/")[-1]
        return form_body_ref


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
                schema.relative_imports.add(_import_string_from_ref(p.ref))
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
    endpoint_collections_by_tag: Dict[str, EndpointCollection]
    enums: Dict[str, EnumProperty]

    @staticmethod
    def from_dict(d: Dict, /) -> OpenAPI:
        """ Create an OpenAPI from dict """
        schemas = Schema.dict(d["components"]["schemas"])
        enums: Dict[str, EnumProperty] = {}
        for schema in schemas.values():
            for prop in schema.properties:
                if not isinstance(prop, EnumProperty):
                    continue
                schema.relative_imports.add(f"from .{prop.name} import {prop.class_name}")
                if prop.class_name in enums:
                    # We already have an enum with this name, make sure the values match
                    assert (
                        prop.values == enums[prop.class_name].values
                    ), f"Encountered conflicting enum named {prop.class_name}"

                enums[prop.class_name] = prop

        return OpenAPI(
            title=d["info"]["title"],
            description=d["info"]["description"],
            version=d["info"]["version"],
            endpoint_collections_by_tag=EndpointCollection.from_dict(d["paths"]),
            schemas=schemas,
            security_schemes=d["components"]["securitySchemes"],
            enums=enums,
        )
