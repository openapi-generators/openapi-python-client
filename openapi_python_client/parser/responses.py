__all__ = ["Response", "response_from_data"]

from http import HTTPStatus
from typing import Optional, TypedDict, Union

from attrs import define
from typing_extensions import TypeAlias

from openapi_python_client import utils
from openapi_python_client.parser.properties.schemas import get_reference_simple_name, parse_reference_path

from .. import Config
from .. import schema as oai
from ..utils import PythonIdentifier
from .errors import ParseError, PropertyError
from .properties import AnyProperty, Property, Schemas, property_from_data


class _ResponseSource(TypedDict):
    """What data should be pulled from the httpx Response object"""

    attribute: str
    return_type: str


JSON_SOURCE = _ResponseSource(attribute="response.json()", return_type="Any")
BYTES_SOURCE = _ResponseSource(attribute="response.content", return_type="bytes")
TEXT_SOURCE = _ResponseSource(attribute="response.text", return_type="str")
NONE_SOURCE = _ResponseSource(attribute="None", return_type="None")

HTTPStatusSpec: TypeAlias = Union[HTTPStatus, tuple[HTTPStatus, int]]
"""Either a single http status or a tuple representing an inclusive range.

The second element of the tuple is also logically a status code but is typically 299 or similar which
is not contained in the enum.

https://github.com/openapi-generators/openapi-python-client/blob/61b6c54994e2a6285bb422ee3b864c45b5d88c15/openapi_python_client/schema/3.1.0.md#responses-object
"""


def http_status_spec(code: str | int) -> HTTPStatusSpec | ParseError:
    """Parses plain integer status codes such as 201 or patterned status codes such as 2XX."""

    multiplier = 1
    if isinstance(code, str):
        if code.endswith("XX"):
            code = code.removesuffix("XX")
            multiplier = 100

    try:
        status_code = int(code)

        if multiplier > 1:
            start = status_code * multiplier
            return (HTTPStatus(start), start + multiplier - 1)

        return HTTPStatus(status_code)
    except ValueError:
        return ParseError(
            detail=(
                f"Invalid response status code {code} (not a valid HTTP "
                f"status code), response will be omitted from generated "
                f"client"
            )
        )


@define
class Response:
    """Describes a single response for an endpoint"""

    status_code: HTTPStatusSpec
    prop: Property
    source: _ResponseSource
    data: Union[oai.Response, oai.Reference]  # Original data which created this response, useful for custom templates


def _source_by_content_type(content_type: str, config: Config) -> Optional[_ResponseSource]:
    parsed_content_type = utils.get_content_type(content_type, config)
    if parsed_content_type is None:
        return None

    if parsed_content_type.startswith("text/"):
        return TEXT_SOURCE

    known_content_types = {
        "application/json": JSON_SOURCE,
        "application/octet-stream": BYTES_SOURCE,
    }
    source = known_content_types.get(parsed_content_type)
    if source is None and parsed_content_type.endswith("+json"):
        # Implements https://www.rfc-editor.org/rfc/rfc6838#section-4.2.8 for the +json suffix
        source = JSON_SOURCE
    return source


def empty_response(
    *,
    status_code: HTTPStatusSpec,
    response_name: str,
    config: Config,
    data: Union[oai.Response, oai.Reference],
) -> Response:
    """Return an untyped response, for when no response type is defined"""
    return Response(
        data=data,
        status_code=status_code,
        prop=AnyProperty(
            name=response_name,
            default=None,
            required=True,
            python_name=PythonIdentifier(value=response_name, prefix=config.field_prefix),
            description=data.description if isinstance(data, oai.Response) else None,
            example=None,
        ),
        source=NONE_SOURCE,
    )


def _status_code_str(status_code_str: str | None, status_code: HTTPStatusSpec) -> str:
    if status_code_str is None:
        if isinstance(status_code, HTTPStatus):
            return str(status_code.value)
        if isinstance(status_code, int):
            return str(status_code)

        raise ValueError(f"status_code_str must be passed for {status_code!r}")

    return status_code_str


def response_from_data(  # noqa: PLR0911
    *,
    status_code_str: str | None = None,
    status_code: HTTPStatusSpec,
    data: Union[oai.Response, oai.Reference],
    schemas: Schemas,
    responses: dict[str, Union[oai.Response, oai.Reference]],
    parent_name: str,
    config: Config,
) -> tuple[Union[Response, ParseError], Schemas]:
    """Generate a Response from the OpenAPI dictionary representation of it"""
    status_code_str = _status_code_str(status_code_str, status_code)

    response_name = f"response_{status_code_str}"
    if isinstance(data, oai.Reference):
        ref_path = parse_reference_path(data.ref)
        if isinstance(ref_path, ParseError):
            return ref_path, schemas
        if not ref_path.startswith("/components/responses/"):
            return ParseError(data=data, detail=f"$ref to {data.ref} not allowed in responses"), schemas
        resp_data = responses.get(get_reference_simple_name(ref_path), None)
        if not resp_data:
            return ParseError(data=data, detail=f"Could not find reference: {data.ref}"), schemas
        if not isinstance(resp_data, oai.Response):
            return ParseError(data=data, detail="Top-level $ref inside components/responses is not supported"), schemas
        data = resp_data

    content = data.content
    if not content:
        return (
            empty_response(
                status_code=status_code,
                response_name=response_name,
                config=config,
                data=data,
            ),
            schemas,
        )

    for content_type, media_type in content.items():
        source = _source_by_content_type(content_type, config)
        if source is not None:
            schema_data = media_type.media_type_schema
            break
    else:
        return (
            ParseError(data=data, detail=f"Unsupported content_type {content}"),
            schemas,
        )

    if schema_data is None:
        return (
            empty_response(
                status_code=status_code,
                response_name=response_name,
                config=config,
                data=data,
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

    return Response(status_code=status_code, prop=prop, source=source, data=data), schemas
