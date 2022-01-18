import re
from collections import OrderedDict
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Dict, Iterator, List, Optional, Set, Tuple, Union

import attr
from pydantic import ValidationError

from .. import schema as oai
from .. import utils
from ..config import Config
from ..utils import PythonIdentifier
from .errors import GeneratorError, ParseError, PropertyError
from .properties import Class, EnumProperty, ModelProperty, Property, Schemas, build_schemas, property_from_data
from .responses import Response, response_from_data

_PATH_PARAM_REGEX = re.compile("{([a-zA-Z_][a-zA-Z0-9_]*)}")


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
    ) -> Tuple[Dict[utils.PythonIdentifier, "EndpointCollection"], Schemas]:
        """Parse the openapi paths data to get EndpointCollections by tag"""
        endpoints_by_tag: Dict[utils.PythonIdentifier, EndpointCollection] = {}

        methods = ["get", "put", "post", "delete", "options", "head", "patch", "trace"]

        for path, path_data in data.items():
            for method in methods:
                operation: Optional[oai.Operation] = getattr(path_data, method)
                if operation is None:
                    continue
                tag = utils.PythonIdentifier(value=(operation.tags or ["default"])[0], prefix="tag")
                collection = endpoints_by_tag.setdefault(tag, EndpointCollection(tag=tag))
                endpoint, schemas = Endpoint.from_data(
                    data=operation, path=path, method=method, tag=tag, schemas=schemas, config=config
                )
                # Add `PathItem` parameters
                if not isinstance(endpoint, ParseError):
                    endpoint, schemas = Endpoint.add_parameters(
                        endpoint=endpoint, data=path_data, schemas=schemas, config=config
                    )
                if not isinstance(endpoint, ParseError):
                    endpoint = Endpoint.sort_parameters(endpoint=endpoint)
                if isinstance(endpoint, ParseError):
                    endpoint.header = (
                        f"WARNING parsing {method.upper()} {path} within {tag}. Endpoint will not be generated."
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


# pylint: disable=too-many-instance-attributes
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
    query_parameters: Dict[str, Property] = field(default_factory=dict)
    path_parameters: "OrderedDict[str, Property]" = field(default_factory=OrderedDict)
    header_parameters: Dict[str, Property] = field(default_factory=dict)
    cookie_parameters: Dict[str, Property] = field(default_factory=dict)
    responses: List[Response] = field(default_factory=list)
    form_body_class: Optional[Class] = None
    json_body: Optional[Property] = None
    multipart_body: Optional[Property] = None
    errors: List[ParseError] = field(default_factory=list)
    used_python_identifiers: Set[PythonIdentifier] = field(default_factory=set)

    @staticmethod
    def parse_request_form_body(*, body: oai.RequestBody, config: Config) -> Optional[Class]:
        """Return form_body_reference"""
        body_content = body.content
        form_body = body_content.get("application/x-www-form-urlencoded")
        if form_body is not None and isinstance(form_body.media_type_schema, oai.Reference):
            return Class.from_string(string=form_body.media_type_schema.ref, config=config)
        return None

    @staticmethod
    def parse_multipart_body(
        *, body: oai.RequestBody, schemas: Schemas, parent_name: str, config: Config
    ) -> Tuple[Union[Property, PropertyError, None], Schemas]:
        """Return multipart_body"""
        body_content = body.content
        multipart_body = body_content.get("multipart/form-data")
        if multipart_body is not None and multipart_body.media_type_schema is not None:
            prop, schemas = property_from_data(
                name="multipart_data",
                required=True,
                data=multipart_body.media_type_schema,
                schemas=schemas,
                parent_name=parent_name,
                config=config,
            )
            if isinstance(prop, ModelProperty):
                prop = attr.evolve(prop, is_multipart_body=True)
                schemas = attr.evolve(schemas, classes_by_name={**schemas.classes_by_name, prop.class_info.name: prop})
            return prop, schemas
        return None, schemas

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
                    header=f"Cannot parse JSON body of endpoint {endpoint.name}",
                    detail=json_body.detail,
                    data=json_body.data,
                ),
                schemas,
            )

        multipart_body, schemas = Endpoint.parse_multipart_body(
            body=data.requestBody, schemas=schemas, parent_name=endpoint.name, config=config
        )
        if isinstance(multipart_body, ParseError):
            return (
                ParseError(
                    header=f"Cannot parse multipart body of endpoint {endpoint.name}",
                    detail=multipart_body.detail,
                    data=multipart_body.data,
                ),
                schemas,
            )

        if endpoint.form_body_class:
            endpoint.relative_imports.add(import_string_from_class(endpoint.form_body_class, prefix="...models"))
        if multipart_body is not None:
            endpoint.multipart_body = multipart_body
            endpoint.relative_imports.update(endpoint.multipart_body.get_imports(prefix="..."))
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

    # pylint: disable=too-many-return-statements
    @staticmethod
    def add_parameters(
        *, endpoint: "Endpoint", data: Union[oai.Operation, oai.PathItem], schemas: Schemas, config: Config
    ) -> Tuple[Union["Endpoint", ParseError], Schemas]:
        """Process the defined `parameters` for an Endpoint.

        Any existing parameters will be ignored, so earlier instances of a parameter take precedence. PathItem
        parameters should therefore be added __after__ operation parameters.

        Args:
            endpoint: The endpoint to add parameters to.
            data: The Operation or PathItem to add parameters from.
            schemas: The cumulative Schemas of processing so far which should contain details for any references.
            config: User-provided config for overrides within parameters.

        Returns:
            `(result, schemas)` where `result` is either an updated Endpoint containing the parameters or a ParseError
                describing what went wrong. `schemas` is an updated version of the `schemas` input, adding any new enums
                or classes.

        See Also:
            - https://swagger.io/docs/specification/describing-parameters/
            - https://swagger.io/docs/specification/paths-and-operations/
        """

        endpoint = deepcopy(endpoint)
        if data.parameters is None:
            return endpoint, schemas

        unique_parameters: Set[Tuple[str, oai.ParameterLocation]] = set()
        parameters_by_location = {
            oai.ParameterLocation.QUERY: endpoint.query_parameters,
            oai.ParameterLocation.PATH: endpoint.path_parameters,
            oai.ParameterLocation.HEADER: endpoint.header_parameters,
            oai.ParameterLocation.COOKIE: endpoint.cookie_parameters,
        }

        for param in data.parameters:
            if isinstance(param, oai.Reference) or param.param_schema is None:
                continue

            unique_param = (param.name, param.param_in)
            if unique_param in unique_parameters:
                duplication_detail = (
                    "Parameters MUST NOT contain duplicates. "
                    "A unique parameter is defined by a combination of a name and location. "
                    f"Duplicated parameters named `{param.name}` detected in `{param.param_in}`."
                )
                return ParseError(data=data, detail=duplication_detail), schemas
            unique_parameters.add(unique_param)

            prop, new_schemas = property_from_data(
                name=param.name,
                required=param.required,
                data=param.param_schema,
                schemas=schemas,
                parent_name=endpoint.name,
                config=config,
            )
            if isinstance(prop, ParseError):
                return ParseError(detail=f"cannot parse parameter of endpoint {endpoint.name}", data=prop.data), schemas
            location_error = prop.validate_location(param.param_in)
            if location_error is not None:
                location_error.data = param
                return location_error, schemas
            schemas = new_schemas
            if prop.name in parameters_by_location[param.param_in]:
                # This parameter was defined in the Operation, so ignore the PathItem definition
                continue

            for location, parameters_dict in parameters_by_location.items():
                if location == param.param_in or prop.name not in parameters_dict:
                    continue
                existing_prop: Property = parameters_dict[prop.name]
                # Existing should be converted too for consistency
                endpoint.used_python_identifiers.remove(existing_prop.python_name)
                existing_prop.set_python_name(new_name=f"{existing_prop.name}_{location}", config=config)

                if existing_prop.python_name in endpoint.used_python_identifiers:
                    return (
                        ParseError(
                            detail=f"Parameters with same Python identifier `{existing_prop.python_name}` detected",
                            data=data,
                        ),
                        schemas,
                    )
                endpoint.used_python_identifiers.add(existing_prop.python_name)
                prop.set_python_name(new_name=f"{param.name}_{param.param_in}", config=config)

            if prop.python_name in endpoint.used_python_identifiers:
                return (
                    ParseError(
                        detail=f"Parameters with same Python identifier `{prop.python_name}` detected", data=data
                    ),
                    schemas,
                )
            if param.param_in == oai.ParameterLocation.QUERY and (prop.nullable or not prop.required):
                # There is no NULL for query params, so nullable and not required are the same.
                prop = attr.evolve(prop, required=False, nullable=True)

            endpoint.relative_imports.update(prop.get_imports(prefix="..."))
            endpoint.used_python_identifiers.add(prop.python_name)
            parameters_by_location[param.param_in][prop.name] = prop

        return endpoint, schemas

    @staticmethod
    def sort_parameters(*, endpoint: "Endpoint") -> Union["Endpoint", ParseError]:
        """
        Sorts the path parameters of an `endpoint` so that they match the order declared in `endpoint.path`.

        Args:
            endpoint: The endpoint to sort the parameters of.

        Returns:
            Either an updated `endpoint` with sorted path parameters or a `ParseError` if something was wrong with
                the path parameters and they could not be sorted.
        """
        endpoint = deepcopy(endpoint)
        parameters_from_path = re.findall(_PATH_PARAM_REGEX, endpoint.path)
        try:
            sorted_params = sorted(
                endpoint.path_parameters.values(), key=lambda param: parameters_from_path.index(param.name)
            )
            endpoint.path_parameters = OrderedDict((param.name, param) for param in sorted_params)
        except ValueError:
            pass  # We're going to catch the difference down below

        if parameters_from_path != list(endpoint.path_parameters):
            return ParseError(
                detail=f"Incorrect path templating for {endpoint.path} (Path parameters do not match with path)",
            )
        return endpoint

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

        result, schemas = Endpoint.add_parameters(endpoint=endpoint, data=data, schemas=schemas, config=config)
        if isinstance(result, ParseError):
            return result, schemas
        result, schemas = Endpoint._add_responses(endpoint=result, data=data.responses, schemas=schemas, config=config)
        result, schemas = Endpoint._add_body(endpoint=result, data=data, schemas=schemas, config=config)

        return result, schemas

    def response_type(self) -> str:
        """Get the Python type of any response from this endpoint"""
        types = sorted({response.prop.get_type_string() for response in self.responses})
        if len(types) == 0:
            return "Any"
        if len(types) == 1:
            return self.responses[0].prop.get_type_string()
        return f"Union[{', '.join(types)}]"

    def iter_all_parameters(self) -> Iterator[Property]:
        """Iterate through all the parameters of this endpoint"""
        yield from self.path_parameters.values()
        yield from self.query_parameters.values()
        yield from self.header_parameters.values()
        yield from self.cookie_parameters.values()
        if self.multipart_body:
            yield self.multipart_body
        if self.json_body:
            yield self.json_body

    def list_all_parameters(self) -> List[Property]:
        """Return a List of all the parameters of this endpoint"""
        return list(self.iter_all_parameters())


@dataclass
class GeneratorData:
    """All the data needed to generate a client"""

    title: str
    description: Optional[str]
    version: str
    models: Iterator[ModelProperty]
    errors: List[ParseError]
    endpoint_collections_by_tag: Dict[utils.PythonIdentifier, EndpointCollection]
    enums: Iterator[EnumProperty]

    @staticmethod
    def from_dict(data: Dict[str, Any], *, config: Config) -> Union["GeneratorData", GeneratorError]:
        """Create an OpenAPI from dict"""
        try:
            openapi = oai.OpenAPI.parse_obj(data)
        except ValidationError as err:
            detail = str(err)
            if "swagger" in data:
                detail = (
                    "You may be trying to use a Swagger document; this is not supported by this project.\n\n" + detail
                )
            return GeneratorError(header="Failed to parse OpenAPI document", detail=detail)
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
