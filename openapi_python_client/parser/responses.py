__all__ = ["Response", "response_from_data"]

from typing import Optional, Tuple, Union

import attr

from .. import Config
from .. import schema as oai
from ..utils import PythonIdentifier
from .errors import ParseError, PropertyError
from .properties import AnyProperty, Property, Schemas, property_from_data


@attr.s(auto_attribs=True, frozen=True)
class Response:
    """Describes a single response for an endpoint"""

    status_code: int
    prop: Property
    source: str


_SOURCE_BY_CONTENT_TYPE = {
    "application/json": "response.json()",
    "application/vnd.api+json": "response.json()",
    "application/octet-stream": "response.content",
    "text/html": "response.text",
}


def empty_response(*, status_code: int, response_name: str, config: Config, description: Optional[str]) -> Response:
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
    *, status_code: int, data: Union[oai.Response, oai.Reference], schemas: Schemas, parent_name: str, config: Config
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
        if content_type in _SOURCE_BY_CONTENT_TYPE:
            source = _SOURCE_BY_CONTENT_TYPE[content_type]
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

    return Response(status_code=status_code, prop=prop, source=source), schemas
