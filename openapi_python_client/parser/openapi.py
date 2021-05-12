import itertools
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Dict, Iterator, List, Optional, Set, Tuple, Union

from pydantic import ValidationError

from .. import schema as oai
from .. import utils
from ..config import Config
from .errors import GeneratorError, ParseError, PropertyError
from .properties import Class, EnumProperty, ModelProperty, Property, Schemas, build_schemas, property_from_data
from .responses import Response, response_from_data


def import_string_from_class(class_: Class, prefix: str = "") -> str:
    """Create a string which is used to import a reference"""
    return f"from {prefix}.{class_.module_name} import {class_.name}"


@dataclass
class EndpointCollection:
    """A bunch of endpoints grouped under a tag that will become a module"""

    tag: str
    endpoints: List["Endpoint"] = field(default_factory=list)
    parse_errors: List[ParseError] = field(default_factory=list)

    @staticmethod
    def from_data(
        *, data: Dict[str, oai.PathItem], schemas: Schemas, config: Config
    ) -> Tuple[Dict[str, "EndpointCollection"], Schemas]:
        """Parse the openapi paths data to get EndpointCollections by tag"""
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
                    data=operation, path=path, method=method, tag=tag, schemas=schemas, config=config
                )
                if not isinstance(endpoint, ParseError):
                    endpoint, schemas = Endpoint._add_parameters(
                        endpoint=endpoint, data=path_data, schemas=schemas, config=config
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
    """Generate an operationId from a path"""
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
    summary: Optional[str] = ""
    relative_imports: Set[str] = field(default_factory=set)
    query_parameters: List[Property] = field(default_factory=list)
    path_parameters: List[Property] = field(default_factory=list)
    header_parameters: List[Property] = field(default_factory=list)
    cookie_parameters: List[Property] = field(default_factory=list)
    responses: List[Response] = field(default_factory=list)
    form_body_class: Optional[Class] = None
    json_body: Optional[Property] = None
    multipart_body_class: Optional[Class] = None
    errors: List[ParseError] = field(default_factory=list)

    @staticmethod
    def parse_request_form_body(*, body: oai.RequestBody, config: Config) -> Optional[Class]:
        """Return form_body_reference"""
        body_content = body.content
        form_body = body_content.get("application/x-www-form-urlencoded")
        if form_body is not None and isinstance(form_body.media_type_schema, oai.Reference):
            return Class.from_string(string=form_body.media_type_schema.ref, config=config)
        return None

    @staticmethod
    def parse_multipart_body(*, body: oai.RequestBody, config: Config) -> Optional[Class]:
        """Return form_body_reference"""
        body_content = body.content
        json_body = body_content.get("multipart/form-data")
        if json_body is not None and isinstance(json_body.media_type_schema, oai.Reference):
            return Class.from_string(string=json_body.media_type_schema.ref, config=config)
        return None

    @staticmethod
    def parse_request_json_body(
        *, body: oai.RequestBody, schemas: Schemas, parent_name: str, config: Config
    ) -> Tuple[Union[Property, PropertyError, None], Schemas]:
        """Return json_body"""
        body_content = body.content
        json_body = body_content.get("application/json")
        if json_body is not None and json_body.media_type_schema is not None:
            return property_from_data(
                name="json_body",
                required=True,
                data=json_body.media_type_schema,
                schemas=schemas,
                parent_name=parent_name,
                config=config,
            )
        return None, schemas

    @staticmethod
    def _add_body(
        *,
        endpoint: "Endpoint",
        data: oai.Operation,
        schemas: Schemas,
        config: Config,
    ) -> Tuple[Union[ParseError, "Endpoint"], Schemas]:
        """Adds form or JSON body to Endpoint if included in data"""
        endpoint = deepcopy(endpoint)
        if data.requestBody is None or isinstance(data.requestBody, oai.Reference):
            return endpoint, schemas

        endpoint.form_body_class = Endpoint.parse_request_form_body(body=data.requestBody, config=config)
        json_body, schemas = Endpoint.parse_request_json_body(
            body=data.requestBody, schemas=schemas, parent_name=endpoint.name, config=config
        )
        if isinstance(json_body, ParseError):
            return (
                ParseError(
                    header=f"Cannot parse body of endpoint {endpoint.name}",
                    detail=json_body.detail,
                    data=json_body.data,
                ),
                schemas,
            )

        endpoint.multipart_body_class = Endpoint.parse_multipart_body(body=data.requestBody, config=config)

        if endpoint.form_body_class:
            endpoint.relative_imports.add(import_string_from_class(endpoint.form_body_class, prefix="...models"))
        if endpoint.multipart_body_class:
            endpoint.relative_imports.add(import_string_from_class(endpoint.multipart_body_class, prefix="...models"))
        if json_body is not None:
            endpoint.json_body = json_body
            endpoint.relative_imports.update(endpoint.json_body.get_imports(prefix="..."))
        return endpoint, schemas

    @staticmethod
    def _add_responses(
        *, endpoint: "Endpoint", data: oai.Responses, schemas: Schemas, config: Config
    ) -> Tuple["Endpoint", Schemas]:
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
                status_code=status_code, data=response_data, schemas=schemas, parent_name=endpoint.name, config=config
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
        *, endpoint: "Endpoint", data: Union[oai.Operation, oai.PathItem], schemas: Schemas, config: Config
    ) -> Tuple[Union["Endpoint", ParseError], Schemas]:
        endpoint = deepcopy(endpoint)
        used_python_names: Dict[str, Tuple[Property, oai.ParameterLocation]] = {}
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
                config=config,
            )
            if isinstance(prop, ParseError):
                return ParseError(detail=f"cannot parse parameter of endpoint {endpoint.name}", data=prop.data), schemas

            if prop.python_name in used_python_names:
                duplicate, duplicate_location = used_python_names[prop.python_name]
                if duplicate.python_name == prop.python_name:  # Existing should be converted too for consistency
                    duplicate.set_python_name(f"{duplicate.python_name}_{duplicate_location}")
                prop.set_python_name(f"{prop.python_name}_{param.param_in}")
            else:
                used_python_names[prop.python_name] = (prop, param.param_in)

            endpoint.relative_imports.update(prop.get_imports(prefix="..."))

            if param.param_in == oai.ParameterLocation.QUERY:
                endpoint.query_parameters.append(prop)
            elif param.param_in == oai.ParameterLocation.PATH:
                endpoint.path_parameters.append(prop)
            elif param.param_in == oai.ParameterLocation.HEADER:
                endpoint.header_parameters.append(prop)
            elif param.param_in == oai.ParameterLocation.COOKIE:
                endpoint.cookie_parameters.append(prop)
            else:
                return ParseError(data=param, detail="Parameter must be declared in path or query"), schemas

        name_check = set()
        for prop in itertools.chain(
            endpoint.query_parameters, endpoint.path_parameters, endpoint.header_parameters, endpoint.cookie_parameters
        ):
            if prop.python_name in name_check:
                return (
                    ParseError(data=data, detail=f"Could not reconcile duplicate parameters named {prop.python_name}"),
                    schemas,
                )
            name_check.add(prop.python_name)

        return endpoint, schemas

    @staticmethod
    def from_data(
        *, data: oai.Operation, path: str, method: str, tag: str, schemas: Schemas, config: Config
    ) -> Tuple[Union["Endpoint", ParseError], Schemas]:
        """Construct an endpoint from the OpenAPI data"""

        if data.operationId is None:
            name = generate_operation_id(path=path, method=method)
        else:
            name = data.operationId

        endpoint = Endpoint(
            path=path,
            method=method,
            summary=utils.remove_string_escapes(data.summary) if data.summary else "",
            description=utils.remove_string_escapes(data.description) if data.description else "",
            name=name,
            requires_security=bool(data.security),
            tag=tag,
        )

        result, schemas = Endpoint._add_parameters(endpoint=endpoint, data=data, schemas=schemas, config=config)
        if isinstance(result, ParseError):
            return result, schemas
        result, schemas = Endpoint._add_responses(endpoint=result, data=data.responses, schemas=schemas, config=config)
        result, schemas = Endpoint._add_body(endpoint=result, data=data, schemas=schemas, config=config)

        return result, schemas

    def response_type(self) -> str:
        """Get the Python type of any response from this endpoint"""
        types = sorted({response.prop.get_type_string() for response in self.responses})
        if len(types) == 0:
            return "None"
        if len(types) == 1:
            return self.responses[0].prop.get_type_string()
        return f"Union[{', '.join(types)}]"


@dataclass
class GeneratorData:
    """All the data needed to generate a client"""

    title: str
    description: Optional[str]
    version: str
    models: Iterator[ModelProperty]
    errors: List[ParseError]
    endpoint_collections_by_tag: Dict[str, EndpointCollection]
    enums: Iterator[EnumProperty]

    @staticmethod
    def from_dict(d: Dict[str, Any], *, config: Config) -> Union["GeneratorData", GeneratorError]:
        """Create an OpenAPI from dict"""
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
        schemas = Schemas()
        if openapi.components and openapi.components.schemas:
            schemas = build_schemas(components=openapi.components.schemas, schemas=schemas, config=config)
        endpoint_collections_by_tag, schemas = EndpointCollection.from_data(
            data=openapi.paths, schemas=schemas, config=config
        )

        enums = (prop for prop in schemas.classes_by_name.values() if isinstance(prop, EnumProperty))
        models = (prop for prop in schemas.classes_by_name.values() if isinstance(prop, ModelProperty))

        return GeneratorData(
            title=openapi.info.title,
            description=openapi.info.description,
            version=openapi.info.version,
            endpoint_collections_by_tag=endpoint_collections_by_tag,
            models=models,
            errors=schemas.errors,
            enums=enums,
        )
