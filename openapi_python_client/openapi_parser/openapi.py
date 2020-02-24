from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Generator, Iterable, List, Optional, Set

from .properties import EnumProperty, ListProperty, Property, RefProperty, property_from_dict
from .reference import Reference
from .responses import ListRefResponse, RefResponse, Response, response_from_dict


class ParameterLocation(str, Enum):
    """ The places Parameters can be put when calling an Endpoint """

    QUERY = "query"
    PATH = "path"


def import_string_from_reference(reference: Reference, prefix: str = "") -> str:
    """ Create a string which is used to import a reference """
    return f"from {prefix}.{reference.module_name} import {reference.class_name}"


@dataclass
class EndpointCollection:
    """ A bunch of endpoints grouped under a tag that will become a module """

    tag: str
    endpoints: List[Endpoint] = field(default_factory=list)
    relative_imports: Set[str] = field(default_factory=set)

    @staticmethod
    def from_dict(d: Dict[str, Dict[str, Dict[str, Any]]], /) -> Dict[str, EndpointCollection]:
        """ Parse the openapi paths data to get EndpointCollections by tag """
        endpoints_by_tag: Dict[str, EndpointCollection] = {}
        for path, path_data in d.items():
            for method, method_data in path_data.items():
                query_parameters: List[Property] = []
                path_parameters: List[Property] = []
                responses: List[Response] = []
                tag = method_data.get("tags", ["default"])[0]
                collection = endpoints_by_tag.setdefault(tag, EndpointCollection(tag=tag))
                for param_dict in method_data.get("parameters", []):
                    prop = property_from_dict(
                        name=param_dict["name"], required=param_dict["required"], data=param_dict["schema"]
                    )
                    if isinstance(prop, (ListProperty, RefProperty, EnumProperty)) and prop.reference:
                        collection.relative_imports.add(import_string_from_reference(prop.reference, prefix="..models"))
                    if param_dict["in"] == ParameterLocation.QUERY:
                        query_parameters.append(prop)
                    elif param_dict["in"] == ParameterLocation.PATH:
                        path_parameters.append(prop)
                    else:
                        raise ValueError(f"Don't know where to put this parameter: {param_dict}")

                for code, response_dict in method_data["responses"].items():
                    response = response_from_dict(status_code=int(code), data=response_dict)
                    if isinstance(response, (RefResponse, ListRefResponse)):
                        collection.relative_imports.add(
                            import_string_from_reference(response.reference, prefix="..models")
                        )
                    responses.append(response)
                form_body_reference = None
                json_body = None
                if "requestBody" in method_data:
                    form_body_reference = Endpoint.parse_request_form_body(method_data["requestBody"])
                    json_body = Endpoint.parse_request_json_body(method_data["requestBody"])

                endpoint = Endpoint(
                    path=path,
                    method=method,
                    description=method_data.get("description"),
                    name=method_data["operationId"],
                    query_parameters=query_parameters,
                    path_parameters=path_parameters,
                    responses=responses,
                    form_body_reference=form_body_reference,
                    json_body=json_body,
                    requires_security=bool(method_data.get("security")),
                )

                collection.endpoints.append(endpoint)
                if form_body_reference:
                    collection.relative_imports.add(
                        import_string_from_reference(form_body_reference, prefix="..models")
                    )
                if (
                    json_body is not None
                    and isinstance(json_body, (ListProperty, RefProperty, EnumProperty))
                    and json_body.reference is not None
                ):
                    collection.relative_imports.add(
                        import_string_from_reference(json_body.reference, prefix="..models")
                    )
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
    query_parameters: List[Property]
    path_parameters: List[Property]
    responses: List[Response]
    requires_security: bool
    form_body_reference: Optional[Reference]
    json_body: Optional[Property]

    @staticmethod
    def parse_request_form_body(body: Dict[str, Any], /) -> Optional[Reference]:
        """ Return form_body_reference """
        body_content = body["content"]
        form_body = body_content.get("application/x-www-form-urlencoded")
        if form_body:
            return Reference(form_body["schema"]["$ref"])
        return None

    @staticmethod
    def parse_request_json_body(body: Dict[str, Any], /) -> Optional[Property]:
        """ Return json_body """
        body_content = body["content"]
        json_body = body_content.get("application/json")
        if json_body:
            return property_from_dict("json_body", required=True, data=json_body["schema"])
        return None


@dataclass
class Schema:
    """
    Describes a schema, AKA data model used in requests.

    These will all be converted to dataclasses in the client
    """

    reference: Reference
    required_properties: List[Property]
    optional_properties: List[Property]
    description: str
    relative_imports: Set[str]

    @staticmethod
    def from_dict(d: Dict[str, Any], /) -> Schema:
        """ A single Schema from its dict representation """
        required_set = set(d.get("required", []))
        required_properties: List[Property] = []
        optional_properties: List[Property] = []
        relative_imports: Set[str] = set()

        for key, value in d["properties"].items():
            required = key in required_set
            p = property_from_dict(name=key, required=required, data=value)
            if required:
                required_properties.append(p)
            else:
                optional_properties.append(p)
            if isinstance(p, (ListProperty, RefProperty, EnumProperty)) and p.reference:
                relative_imports.add(import_string_from_reference(p.reference))
        schema = Schema(
            reference=Reference(d["title"]),
            required_properties=required_properties,
            optional_properties=optional_properties,
            relative_imports=relative_imports,
            description=d.get("description", ""),
        )
        return schema

    @staticmethod
    def dict(d: Dict[str, Dict[str, Any]], /) -> Dict[str, Schema]:
        """ Get a list of Schemas from an OpenAPI dict """
        result = {}
        for data in d.values():
            s = Schema.from_dict(data)
            result[s.reference.class_name] = s
        return result


@dataclass
class OpenAPI:
    """ Top level OpenAPI spec """

    title: str
    description: str
    version: str
    schemas: Dict[str, Schema]
    endpoint_collections_by_tag: Dict[str, EndpointCollection]
    enums: Dict[str, EnumProperty]

    @staticmethod
    def _check_enums(schemas: Iterable[Schema], collections: Iterable[EndpointCollection]) -> Dict[str, EnumProperty]:
        """
        Create EnumProperties for every enum in any schema or collection.
        Enums are deduplicated by class name.

        :raises AssertionError: if two Enums with the same name but different values are detected
        """
        enums: Dict[str, EnumProperty] = {}

        def _iterate_properties() -> Generator[Property, None, None]:
            for schema in schemas:
                yield from schema.required_properties
                yield from schema.optional_properties
            for collection in collections:
                for endpoint in collection.endpoints:
                    yield from endpoint.path_parameters
                    yield from endpoint.query_parameters

        for prop in _iterate_properties():
            if not isinstance(prop, EnumProperty):
                continue

            if prop.reference.class_name in enums:
                # We already have an enum with this name, make sure the values match
                assert (
                    prop.values == enums[prop.reference.class_name].values
                ), f"Encountered conflicting enum named {prop.reference.class_name}"

            enums[prop.reference.class_name] = prop
        return enums

    @staticmethod
    def from_dict(d: Dict[str, Dict[str, Any]], /) -> OpenAPI:
        """ Create an OpenAPI from dict """
        schemas = Schema.dict(d["components"]["schemas"])
        endpoint_collections_by_tag = EndpointCollection.from_dict(d["paths"])
        enums = OpenAPI._check_enums(schemas.values(), endpoint_collections_by_tag.values())

        return OpenAPI(
            title=d["info"]["title"],
            description=d["info"]["description"],
            version=d["info"]["version"],
            endpoint_collections_by_tag=endpoint_collections_by_tag,
            schemas=schemas,
            enums=enums,
        )
