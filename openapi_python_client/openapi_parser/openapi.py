from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Generator, Iterable, List, Optional, Set, Union

from .properties import EnumListProperty, EnumProperty, Property, ReferenceListProperty, RefProperty, property_from_dict
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
                endpoint = Endpoint.from_data(data=method_data, path=path, method=method)
                collection = endpoints_by_tag.setdefault(endpoint.tag, EndpointCollection(tag=endpoint.tag))
                collection.endpoints.append(endpoint)
                collection.relative_imports.update(endpoint.relative_imports)
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
    requires_security: bool
    tag: str
    relative_imports: Set[str] = field(default_factory=set)
    query_parameters: List[Property] = field(default_factory=list)
    path_parameters: List[Property] = field(default_factory=list)
    responses: List[Response] = field(default_factory=list)
    form_body_reference: Optional[Reference] = None
    json_body: Optional[Property] = None

    @staticmethod
    def parse_request_form_body(body: Dict[str, Any], /) -> Optional[Reference]:
        """ Return form_body_reference """
        body_content = body["content"]
        form_body = body_content.get("application/x-www-form-urlencoded")
        if form_body:
            return Reference.from_ref(form_body["schema"]["$ref"])
        return None

    @staticmethod
    def parse_request_json_body(body: Dict[str, Any], /) -> Optional[Property]:
        """ Return json_body """
        body_content = body["content"]
        json_body = body_content.get("application/json")
        if json_body:
            return property_from_dict("json_body", required=True, data=json_body["schema"])
        return None

    def _add_body(self, data: Dict[str, Any]) -> None:
        """ Adds form or JSON body to Endpoint if included in data """
        if "requestBody" not in data:
            return

        self.form_body_reference = Endpoint.parse_request_form_body(data["requestBody"])
        self.json_body = Endpoint.parse_request_json_body(data["requestBody"])

        if self.form_body_reference:
            self.relative_imports.add(import_string_from_reference(self.form_body_reference, prefix="..models"))
        if (
            self.json_body is not None
            and isinstance(self.json_body, (ReferenceListProperty, EnumListProperty, RefProperty, EnumProperty))
            and self.json_body.reference is not None
        ):
            self.relative_imports.add(import_string_from_reference(self.json_body.reference, prefix="..models"))

    def _add_responses(self, data: Dict[str, Any]) -> None:
        for code, response_dict in data["responses"].items():
            response = response_from_dict(status_code=int(code), data=response_dict)
            if isinstance(response, (RefResponse, ListRefResponse)):
                self.relative_imports.add(import_string_from_reference(response.reference, prefix="..models"))
            self.responses.append(response)

    def _add_parameters(self, data: Dict[str, Any]) -> None:
        for param_dict in data.get("parameters", []):
            prop = property_from_dict(
                name=param_dict["name"], required=param_dict["required"], data=param_dict["schema"]
            )
            if (
                isinstance(prop, (ReferenceListProperty, EnumListProperty, RefProperty, EnumProperty))
                and prop.reference
            ):
                self.relative_imports.add(import_string_from_reference(prop.reference, prefix="..models"))
            if param_dict["in"] == ParameterLocation.QUERY:
                self.query_parameters.append(prop)
            elif param_dict["in"] == ParameterLocation.PATH:
                self.path_parameters.append(prop)
            else:
                raise ValueError(f"Don't know where to put this parameter: {param_dict}")

    @staticmethod
    def from_data(*, data: Dict[str, Any], path: str, method: str) -> Endpoint:
        """ Construct an endpoint from the OpenAPI data """

        endpoint = Endpoint(
            path=path,
            method=method,
            description=data.get("description"),
            name=data["operationId"],
            requires_security=bool(data.get("security")),
            tag=data.get("tags", ["default"])[0],
        )
        endpoint._add_parameters(data)
        endpoint._add_responses(data)
        endpoint._add_body(data)

        return endpoint


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
            if isinstance(p, (ReferenceListProperty, EnumListProperty, RefProperty, EnumProperty)) and p.reference:
                relative_imports.add(import_string_from_reference(p.reference))
        schema = Schema(
            reference=Reference.from_ref(d["title"]),
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
    enums: Dict[str, Union[EnumProperty, EnumListProperty]]

    @staticmethod
    def _check_enums(
        schemas: Iterable[Schema], collections: Iterable[EndpointCollection]
    ) -> Dict[str, Union[EnumProperty, EnumListProperty]]:
        """
        Create EnumProperties for every enum in any schema or collection.
        Enums are deduplicated by class name.

        :raises AssertionError: if two Enums with the same name but different values are detected
        """
        enums: Dict[str, Union[EnumProperty, EnumListProperty]] = {}

        def _iterate_properties() -> Generator[Property, None, None]:
            for schema in schemas:
                yield from schema.required_properties
                yield from schema.optional_properties
            for collection in collections:
                for endpoint in collection.endpoints:
                    yield from endpoint.path_parameters
                    yield from endpoint.query_parameters

        for prop in _iterate_properties():
            if not isinstance(prop, (EnumProperty, EnumListProperty)):
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
