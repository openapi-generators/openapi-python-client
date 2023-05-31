__all__ = ["Response", "response_from_data"]

from http import HTTPStatus
from typing import Optional, Tuple, Union, Dict, Sequence, TYPE_CHECKING, Set
from dataclasses import dataclass

import attr

from .. import Config
from .. import schema as oai
from ..utils import PythonIdentifier, count_by_length
from .errors import ParseError, PropertyError
from .properties import AnyProperty, Property, Schemas, property_from_data, ModelProperty
from .traverse_model import traverse_properties

if TYPE_CHECKING:
    from .endpoint_collection import Endpoints, Endpoint


@dataclass
class DataPropertyPath:
    """Describes a json path to a property"""

    path: Tuple[str, ...]
    prop: ModelProperty

    def __str__(self) -> str:
        return f"DataPropertyPath {self.path}: {self.prop.class_info.name}"


@attr.s(auto_attribs=True)
class Response:
    """Describes a single response for an endpoint"""

    status_code: HTTPStatus
    prop: Property
    source: str
    list_properties: Dict[Tuple[str, ...], ModelProperty] = attr.ib(factory=dict)
    """Mapping of json path to model of all array-of-object properties"""
    model_properties: Dict[Tuple[str, ...], ModelProperty] = attr.ib(factory=dict)
    """Mapping of json path to model of all model properties referenced in the response"""
    list_property: Optional[DataPropertyPath] = None
    """The most likely candidate for data list property in the response"""


def _source_by_content_type(content_type: str) -> Optional[str]:
    known_content_types = {
        "application/json": "response.json()",
        "application/octet-stream": "response.content",
        "text/html": "response.text",
    }
    source = known_content_types.get(content_type)
    if source is None and content_type.endswith("+json"):
        # Implements https://www.rfc-editor.org/rfc/rfc6838#section-4.2.8 for the +json suffix
        source = "response.json()"
    return source


def process_responses(schemas: Schemas, endpoints: "Endpoints"):
    """Process all responses in schemas"""
    # First pass identify all list properties
    for endpoint in endpoints.endpoints_by_name.values():
        for response in endpoint.responses:
            # for responses in schemas.responses_by_endpoint.values():
            #     for response in responses:
            lists, models = traverse_properties(response.prop)
            response.list_properties.update(lists)
            response.model_properties.update(models)

    class_name_to_endpoints: Dict[str, Set["Endpoint"]] = {}
    for endpoint in endpoints.endpoints_by_name.values():
        for response in endpoint.responses:
            # for endpoint_name, responses in schemas.responses_by_endpoint.items():
            #     for response in responses:
            for prop in response.model_properties.values():
                items = class_name_to_endpoints.setdefault(prop.class_info.name, set())
                items.add(endpoints.endpoints_by_name[endpoint.name])

    all_endpoints = list(endpoints.endpoints_by_name.values())
    for endpoint in all_endpoints:
        resp = endpoint.responses[0]
        _process_response_list(resp, endpoint, endpoints, class_name_to_endpoints)
    return


def _process_response_list(
    response: Response,
    endpoint: "Endpoint",
    endpoints: "Endpoints",
    class_name_to_endpoints: Dict[str, Set["Endpoint"]],
):
    if not response.list_properties:
        return
    if () in response.list_properties:  # Response is a top level list
        response.list_property = DataPropertyPath((), response.list_properties[()])
        return

    level_counts = count_by_length(response.list_properties.keys())

    # Get list properties max 2 levels down
    props_first_levels = [
        (path, prop) for path, prop in sorted(response.list_properties.items(), key=lambda k: len(k)) if len(path) <= 2
    ]

    # If there is only one list property 1 or 2 levels down, this is the list
    for path, prop in props_first_levels:
        levels = len(path)
        if level_counts[levels] == 1:
            response.list_property = DataPropertyPath(path, prop)
    parent = endpoints.find_immediate_parent(endpoint.path)
    if parent and not parent.has_path_parameters:
        response.list_property = None
    return

    for path, list_prop in response.list_properties.items():
        model_name = list_prop.class_info.name
        # Other endpoints referencing this same model
        other_endpoints = class_name_to_endpoints[model_name] - {endpoint}
        for other_ep in other_endpoints:
            if other_ep.has_path_parameters:
                response.list_property = DataPropertyPath(path, list_prop)
                return

    # Second pass to find THE list property for all the responses
    # # Second pass only success responses
    # for endpoint, responses in schemas.responses_by_endpoint.items():
    #     for response in responses:
    #         response.list_properties.update(traverse_properties(response.prop))


def empty_response(
    *, status_code: HTTPStatus, response_name: str, config: Config, description: Optional[str]
) -> Response:
    """Return an untyped response, for when no response type is defined"""
    return Response(
        status_code=status_code,
        prop=AnyProperty(
            name=response_name,
            default=None,
            nullable=False,
            required=True,
            python_name=PythonIdentifier(value=response_name, prefix=config.field_prefix),
            description=description,
            example=None,
        ),
        source="None",
    )


def response_from_data(
    *,
    status_code: HTTPStatus,
    data: Union[oai.Response, oai.Reference],
    schemas: Schemas,
    parent_name: str,
    config: Config,
) -> Tuple[Union[Response, ParseError], Schemas]:
    """Generate a Response from the OpenAPI dictionary representation of it"""

    response_name = f"response_{status_code}"
    if isinstance(data, oai.Reference):
        return (
            empty_response(status_code=status_code, response_name=response_name, config=config, description=None),
            schemas,
        )

    content = data.content
    if not content:
        return (
            empty_response(
                status_code=status_code, response_name=response_name, config=config, description=data.description
            ),
            schemas,
        )

    for content_type, media_type in content.items():
        source = _source_by_content_type(content_type)
        if source is not None:
            schema_data = media_type.media_type_schema
            break
    else:
        return ParseError(data=data, detail=f"Unsupported content_type {content}"), schemas

    if schema_data is None:
        return (
            empty_response(
                status_code=status_code, response_name=response_name, config=config, description=data.description
            ),
            schemas,
        )

    prop, schemas = property_from_data(
        name=response_name,
        required=True,
        data=schema_data,
        schemas=schemas,
        parent_name=parent_name,
        config=config,
    )

    if isinstance(prop, PropertyError):
        return prop, schemas

    resp = Response(status_code=status_code, prop=prop, source=source)
    # current = schemas.responses_by_endpoint.get(parent_name, [])
    # schemas = attr.evolve(
    #     schemas, responses_by_endpoint={**schemas.responses_by_endpoint, parent_name: current + [resp]}
    # )
    return resp, schemas
