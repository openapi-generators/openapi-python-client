from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Union

import openapi_schema_pydantic as oai

from .errors import ParseError
from .properties import EnumProperty, Property, property_from_data
from .reference import Reference
from .responses import ListRefResponse, RefResponse, Response, response_from_data


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
    parse_errors: List[ParseError] = field(default_factory=list)

    @staticmethod
    def from_data(*, data: Dict[str, oai.PathItem]) -> Dict[str, EndpointCollection]:
        """ Parse the openapi paths data to get EndpointCollections by tag """
        endpoints_by_tag: Dict[str, EndpointCollection] = {}

        methods = ["get", "put", "post", "delete", "options", "head", "patch", "trace"]

        for path, path_data in data.items():
            for method in methods:
                operation: Optional[oai.Operation] = getattr(path_data, method)
                if operation is None:
                    continue
                tag = (operation.tags or ["default"])[0]
                collection = endpoints_by_tag.setdefault(tag, EndpointCollection(tag=tag))
                try:
                    endpoint = Endpoint.from_data(data=operation, path=path, method=method, tag=tag)
                    collection.endpoints.append(endpoint)
                    collection.relative_imports.update(endpoint.relative_imports)
                except ParseError as e:
                    e.header = f"ERROR parsing {method.upper()} {path} within {tag}. Endpoint will not be generated."
                    collection.parse_errors.append(e)

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
    multipart_body_reference: Optional[Reference] = None

    @staticmethod
    def parse_request_form_body(body: oai.RequestBody) -> Optional[Reference]:
        """ Return form_body_reference """
        body_content = body.content
        form_body = body_content.get("application/x-www-form-urlencoded")
        if form_body is not None and isinstance(form_body.media_type_schema, oai.Reference):
            return Reference.from_ref(form_body.media_type_schema.ref)
        return None

    @staticmethod
    def parse_multipart_body(body: oai.RequestBody) -> Optional[Reference]:
        """ Return form_body_reference """
        body_content = body.content
        json_body = body_content.get("multipart/form-data")
        if json_body is not None and isinstance(json_body.media_type_schema, oai.Reference):
            return Reference.from_ref(json_body.media_type_schema.ref)
        return None

    @staticmethod
    def parse_request_json_body(body: oai.RequestBody) -> Optional[Property]:
        """ Return json_body """
        body_content = body.content
        json_body = body_content.get("application/json")
        if json_body is not None and json_body.media_type_schema is not None:
            return property_from_data("json_body", required=True, data=json_body.media_type_schema)
        return None

    def _add_body(self, data: oai.Operation) -> None:
        """ Adds form or JSON body to Endpoint if included in data """
        if data.requestBody is None or isinstance(data.requestBody, oai.Reference):
            return

        self.form_body_reference = Endpoint.parse_request_form_body(data.requestBody)
        self.json_body = Endpoint.parse_request_json_body(data.requestBody)
        self.multipart_body_reference = Endpoint.parse_multipart_body(data.requestBody)

        if self.form_body_reference:
            self.relative_imports.add(import_string_from_reference(self.form_body_reference, prefix="..models"))
        if self.multipart_body_reference:
            self.relative_imports.add(import_string_from_reference(self.multipart_body_reference, prefix="..models"))
        if self.json_body is not None:
            self.relative_imports.update(self.json_body.get_imports(prefix="..models"))

    def _add_responses(self, data: oai.Responses) -> None:
        for code, response_data in data.items():
            response = response_from_data(status_code=int(code), data=response_data)
            if isinstance(response, (RefResponse, ListRefResponse)):
                self.relative_imports.add(import_string_from_reference(response.reference, prefix="..models"))
            self.responses.append(response)

    def _add_parameters(self, data: oai.Operation) -> None:
        if data.parameters is None:
            return
        for param in data.parameters:
            if isinstance(param, oai.Reference) or param.param_schema is None:
                continue
            prop = property_from_data(name=param.name, required=param.required, data=param.param_schema)
            self.relative_imports.update(prop.get_imports(prefix="..models"))

            if param.param_in == ParameterLocation.QUERY:
                self.query_parameters.append(prop)
            elif param.param_in == ParameterLocation.PATH:
                self.path_parameters.append(prop)
            else:
                raise ValueError(f"Don't know where to put this parameter: {param.dict()}")

    @staticmethod
    def from_data(*, data: oai.Operation, path: str, method: str, tag: str) -> Endpoint:
        """ Construct an endpoint from the OpenAPI data """

        if data.operationId is None:
            raise ParseError(data=data, message="Path operations with operationId are not yet supported")

        endpoint = Endpoint(
            path=path,
            method=method,
            description=data.description,
            name=data.operationId,
            requires_security=bool(data.security),
            tag=tag,
        )
        endpoint._add_parameters(data)
        endpoint._add_responses(data.responses)
        endpoint._add_body(data)

        return endpoint


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

    @staticmethod
    def from_data(*, data: Union[oai.Reference, oai.Schema], name: str) -> Model:
        """ A single Model from its OAI data

        Args:
            data: Data of a single Schema
            name: Name by which the schema is referenced, such as a model name.
                Used to infer the type name if a `title` property is not available.
        """
        if isinstance(data, oai.Reference):
            raise ParseError("Reference schemas are not supported.")
        required_set = set(data.required or [])
        required_properties: List[Property] = []
        optional_properties: List[Property] = []
        relative_imports: Set[str] = set()

        ref = Reference.from_ref(data.title or name)

        for key, value in (data.properties or {}).items():
            required = key in required_set
            p = property_from_data(name=key, required=required, data=value)
            if required:
                required_properties.append(p)
            else:
                optional_properties.append(p)
            relative_imports.update(p.get_imports(prefix=""))

        model = Model(
            reference=ref,
            required_properties=required_properties,
            optional_properties=optional_properties,
            relative_imports=relative_imports,
            description=data.description or "",
        )
        return model

    @staticmethod
    def build(*, schemas: Dict[str, Union[oai.Reference, oai.Schema]]) -> Dict[str, Model]:
        """ Get a list of Schemas from an OpenAPI dict """
        result = {}
        for name, data in schemas.items():
            s = Model.from_data(data=data, name=name)
            result[s.reference.class_name] = s
        return result


@dataclass
class GeneratorData:
    """ All the data needed to generate a client """

    title: str
    description: Optional[str]
    version: str
    models: Dict[str, Model]
    endpoint_collections_by_tag: Dict[str, EndpointCollection]
    enums: Dict[str, EnumProperty]

    @staticmethod
    def from_dict(d: Dict[str, Dict[str, Any]]) -> GeneratorData:
        """ Create an OpenAPI from dict """
        openapi = oai.OpenAPI.parse_obj(d)
        if openapi.components is None or openapi.components.schemas is None:
            models = {}
        else:
            models = Model.build(schemas=openapi.components.schemas)
        endpoint_collections_by_tag = EndpointCollection.from_data(data=openapi.paths)
        enums = EnumProperty.get_all_enums()

        return GeneratorData(
            title=openapi.info.title,
            description=openapi.info.description,
            version=openapi.info.version,
            endpoint_collections_by_tag=endpoint_collections_by_tag,
            models=models,
            enums=enums,
        )
