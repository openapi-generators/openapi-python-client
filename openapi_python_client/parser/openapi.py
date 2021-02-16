from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from pydantic import ValidationError

from .. import schema as oai
from .. import utils
from .errors import GeneratorError, ParseError, PropertyError
from .properties import EnumProperty, ModelProperty, Property, Schemas, build_schemas, property_from_data
from .reference import Reference
from .responses import Response, response_from_data


class ParameterLocation(str, Enum):
    """ The places Parameters can be put when calling an Endpoint """

    QUERY = "query"
    PATH = "path"
    HEADER = "header"
    COOKIE = "cookie"


def import_string_from_reference(reference: Reference, prefix: str = "") -> str:
    """ Create a string which is used to import a reference """
    return f"from {prefix}.{reference.module_name} import {reference.class_name}"


@dataclass
class EndpointCollection:
    """ A bunch of endpoints grouped under a tag that will become a module """

    tag: str
    endpoints: List["Endpoint"] = field(default_factory=list)
    parse_errors: List[ParseError] = field(default_factory=list)

    @staticmethod
    def from_data(
        *, data: Dict[str, oai.PathItem], schemas: Schemas
    ) -> Tuple[Dict[str, "EndpointCollection"], Schemas]:
        """ Parse the openapi paths data to get EndpointCollections by tag """
        endpoints_by_tag: Dict[str, EndpointCollection] = {}

        methods = ["get", "put", "post", "delete", "options", "head", "patch", "trace"]

        for path, path_data in data.items():
            for method in methods:
                operation: Optional[oai.Operation] = getattr(path_data, method)
                if operation is None:
                    continue
                tag = utils.snake_case((operation.tags or ["default"])[0])
                collection = endpoints_by_tag.setdefault(tag, EndpointCollection(tag=tag))
                endpoint, schemas = Endpoint.from_data(
                    data=operation, path=path, method=method, tag=tag, schemas=schemas
                )
                if isinstance(endpoint, ParseError):
                    endpoint.header = (
                        f"ERROR parsing {method.upper()} {path} within {tag}. Endpoint will not be generated."
                    )
                    collection.parse_errors.append(endpoint)
                    continue
                for error in endpoint.errors:
                    error.header = f"WARNING parsing {method.upper()} {path} within {tag}."
                    collection.parse_errors.append(error)
                collection.endpoints.append(endpoint)

        return endpoints_by_tag, schemas


def generate_operation_id(*, path: str, method: str) -> str:
    """ Generate an operationId from a path """
    clean_path = path.replace("{", "").replace("}", "").replace("/", "_")
    if clean_path.startswith("_"):
        clean_path = clean_path[1:]
    if clean_path.endswith("_"):
        clean_path = clean_path[:-1]
    return f"{method}_{clean_path}"


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
    header_parameters: List[Property] = field(default_factory=list)
    cookie_parameters: List[Property] = field(default_factory=list)
    responses: List[Response] = field(default_factory=list)
    form_body_reference: Optional[Reference] = None
    json_body: Optional[Property] = None
    multipart_body_reference: Optional[Reference] = None
    errors: List[ParseError] = field(default_factory=list)

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
    def parse_request_json_body(
        *, body: oai.RequestBody, schemas: Schemas, parent_name: str
    ) -> Tuple[Union[Property, PropertyError, None], Schemas]:
        """ Return json_body """
        body_content = body.content
        json_body = body_content.get("application/json")
        if json_body is not None and json_body.media_type_schema is not None:
            return property_from_data(
                name="json_body",
                required=True,
                data=json_body.media_type_schema,
                schemas=schemas,
                parent_name=parent_name,
            )
        return None, schemas

    @staticmethod
    def _add_body(
        *, endpoint: "Endpoint", data: oai.Operation, schemas: Schemas
    ) -> Tuple[Union[ParseError, "Endpoint"], Schemas]:
        """ Adds form or JSON body to Endpoint if included in data """
        endpoint = deepcopy(endpoint)
        if data.requestBody is None or isinstance(data.requestBody, oai.Reference):
            return endpoint, schemas

        endpoint.form_body_reference = Endpoint.parse_request_form_body(data.requestBody)
        json_body, schemas = Endpoint.parse_request_json_body(
            body=data.requestBody, schemas=schemas, parent_name=endpoint.name
        )
        if isinstance(json_body, ParseError):
            return ParseError(detail=f"cannot parse body of endpoint {endpoint.name}", data=json_body.data), schemas

        endpoint.multipart_body_reference = Endpoint.parse_multipart_body(data.requestBody)

        if endpoint.form_body_reference:
            endpoint.relative_imports.add(
                import_string_from_reference(endpoint.form_body_reference, prefix="...models")
            )
        if endpoint.multipart_body_reference:
            endpoint.relative_imports.add(
                import_string_from_reference(endpoint.multipart_body_reference, prefix="...models")
            )
        if json_body is not None:
            endpoint.json_body = json_body
            endpoint.relative_imports.update(endpoint.json_body.get_imports(prefix="..."))
        return endpoint, schemas

    @staticmethod
    def _add_responses(*, endpoint: "Endpoint", data: oai.Responses, schemas: Schemas) -> Tuple["Endpoint", Schemas]:
        endpoint = deepcopy(endpoint)
        for code, response_data in data.items():

            status_code: int
            try:
                status_code = int(code)
            except ValueError:
                endpoint.errors.append(
                    ParseError(
                        detail=(
                            f"Invalid response status code {code} (not a number), "
                            f"response will be ommitted from generated client"
                        )
                    )
                )
                continue

            response, schemas = response_from_data(
                status_code=status_code, data=response_data, schemas=schemas, parent_name=endpoint.name
            )
            if isinstance(response, ParseError):
                endpoint.errors.append(
                    ParseError(
                        detail=(
                            f"Cannot parse response for status code {status_code}, "
                            f"response will be ommitted from generated client"
                        ),
                        data=response.data,
                    )
                )
                continue
            endpoint.relative_imports |= response.prop.get_imports(prefix="...")
            endpoint.responses.append(response)
        return endpoint, schemas

    @staticmethod
    def _add_parameters(
        *, endpoint: "Endpoint", data: oai.Operation, schemas: Schemas
    ) -> Tuple[Union["Endpoint", ParseError], Schemas]:
        endpoint = deepcopy(endpoint)
        if data.parameters is None:
            return endpoint, schemas
        for param in data.parameters:
            if isinstance(param, oai.Reference) or param.param_schema is None:
                continue
            prop, schemas = property_from_data(
                name=param.name,
                required=param.required,
                data=param.param_schema,
                schemas=schemas,
                parent_name=endpoint.name,
            )
            if isinstance(prop, ParseError):
                return ParseError(detail=f"cannot parse parameter of endpoint {endpoint.name}", data=prop.data), schemas
            endpoint.relative_imports.update(prop.get_imports(prefix="..."))

            if param.param_in == ParameterLocation.QUERY:
                endpoint.query_parameters.append(prop)
            elif param.param_in == ParameterLocation.PATH:
                endpoint.path_parameters.append(prop)
            elif param.param_in == ParameterLocation.HEADER:
                endpoint.header_parameters.append(prop)
            elif param.param_in == ParameterLocation.COOKIE:
                endpoint.cookie_parameters.append(prop)
            else:
                return ParseError(data=param, detail="Parameter must be declared in path or query"), schemas
        return endpoint, schemas

    @staticmethod
    def from_data(
        *, data: oai.Operation, path: str, method: str, tag: str, schemas: Schemas
    ) -> Tuple[Union["Endpoint", ParseError], Schemas]:
        """ Construct an endpoint from the OpenAPI data """

        if data.operationId is None:
            name = generate_operation_id(path=path, method=method)
        else:
            name = data.operationId

        endpoint = Endpoint(
            path=path,
            method=method,
            description=utils.remove_string_escapes(data.description) if data.description else "",
            name=name,
            requires_security=bool(data.security),
            tag=tag,
        )

        result, schemas = Endpoint._add_parameters(endpoint=endpoint, data=data, schemas=schemas)
        if isinstance(result, ParseError):
            return result, schemas
        result, schemas = Endpoint._add_responses(endpoint=result, data=data.responses, schemas=schemas)
        result, schemas = Endpoint._add_body(endpoint=result, data=data, schemas=schemas)

        return result, schemas


@dataclass
class GeneratorData:
    """ All the data needed to generate a client """

    title: str
    description: Optional[str]
    version: str
    models: Dict[str, ModelProperty]
    errors: List[ParseError]
    endpoint_collections_by_tag: Dict[str, EndpointCollection]
    enums: Dict[str, EnumProperty]

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> Union["GeneratorData", GeneratorError]:
        """ Create an OpenAPI from dict """
        try:
            openapi = oai.OpenAPI.parse_obj(d)
        except ValidationError as e:
            detail = str(e)
            if "swagger" in d:
                detail = (
                    "You may be trying to use a Swagger document; this is not supported by this project.\n\n" + detail
                )
            return GeneratorError(header="Failed to parse OpenAPI document", detail=detail)
        if openapi.openapi.major != 3:
            return GeneratorError(
                header="openapi-python-client only supports OpenAPI 3.x",
                detail=f"The version of the provided document was {openapi.openapi}",
            )
        if openapi.components is None or openapi.components.schemas is None:
            schemas = Schemas()
        else:
            schemas = build_schemas(components=openapi.components.schemas)
        endpoint_collections_by_tag, schemas = EndpointCollection.from_data(data=openapi.paths, schemas=schemas)
        enums = schemas.enums

        return GeneratorData(
            title=openapi.info.title,
            description=openapi.info.description,
            version=openapi.info.version,
            endpoint_collections_by_tag=endpoint_collections_by_tag,
            models=schemas.models,
            errors=schemas.errors,
            enums=enums,
        )
