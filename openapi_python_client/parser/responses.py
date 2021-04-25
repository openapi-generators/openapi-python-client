__all__ = ["Response", "response_from_data"]

from typing import Tuple, Union

import attr

from .. import Config
from .. import schema as oai
from .errors import ParseError, PropertyError
from .properties import NoneProperty, Property, Schemas, property_from_data


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


def empty_response(status_code: int, response_name: str) -> Response:
    """Return an empty response, for when no response type is defined"""
    return Response(
        status_code=status_code,
        prop=NoneProperty(
            name=response_name,
            default=None,
            nullable=False,
            required=True,
        ),
        source="None",
    )


def response_from_data(
    *, status_code: int, data: Union[oai.Response, oai.Reference], schemas: Schemas, parent_name: str, config: Config
) -> Tuple[Union[Response, ParseError], Schemas]:
    """Generate a Response from the OpenAPI dictionary representation of it"""

    response_name = f"response_{status_code}"
    if isinstance(data, oai.Reference) or data.content is None:
        return (
            empty_response(status_code=status_code, response_name=response_name),
            schemas,
        )

    content = data.content
    for content_type, media_type in content.items():
        if content_type in _SOURCE_BY_CONTENT_TYPE:
            source = _SOURCE_BY_CONTENT_TYPE[content_type]
            schema_data = media_type.media_type_schema
            break
    else:
        return ParseError(data=data, detail=f"Unsupported content_type {content}"), schemas

    if schema_data is None:
        return (
            empty_response(status_code, response_name),
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
