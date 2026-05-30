__all__ = ["HTTPStatusPattern", "Response", "Responses", "response_from_data"]

from collections.abc import Iterator
from typing import TypedDict

from attrs import define

from openapi_python_client import utils
from openapi_python_client.parser.properties.schemas import get_reference_simple_name, parse_reference_path

from .. import Config
from .. import schema as oai
from ..utils import PythonIdentifier
from .errors import ParseError, PropertyError
from .properties import AnyProperty, Property, Schemas, property_from_data


@define
class Responses:
    patterns: list["Response"]
    default: "Response | None"

    def __iter__(self) -> Iterator["Response"]:
        yield from self.patterns
        if self.default:
            yield self.default

    def __len__(self) -> int:
        return len(self.patterns) + (1 if self.default else 0)


class _ResponseSource(TypedDict):
    """What data should be pulled from the httpx Response object"""

    attribute: str
    return_type: str


JSON_SOURCE = _ResponseSource(attribute="response.json()", return_type="Any")
BYTES_SOURCE = _ResponseSource(attribute="response.content", return_type="bytes")
TEXT_SOURCE = _ResponseSource(attribute="response.text", return_type="str")
NONE_SOURCE = _ResponseSource(attribute="None", return_type="None")


class HTTPStatusPattern:
    """Status code patterns come in three flavors, in order of precedence:
    1. Specific status codes, such as 200. This is represented by `min` and `max` being the same.
    2. Ranges of status codes, such as 2XX. This is represented by `min` and `max` being different.
    3. The special `default` status code, which is used when no other status codes match. `range` is `None` in this case.

    https://github.com/openapi-generators/openapi-python-client/blob/61b6c54994e2a6285bb422ee3b864c45b5d88c15/openapi_python_client/schema/3.1.0.md#responses-object
    """

    pattern: str
    range: tuple[int, int] | None

    def __init__(self, *, pattern: str, code_range: tuple[int, int] | None):
        """Initialize with a range of status codes or None for the default case."""
        self.pattern = pattern
        self.range = code_range

    @staticmethod
    def parse(pattern: str) -> "HTTPStatusPattern | ParseError":
        """Parse a status code pattern such as 2XX or 404"""
        if pattern == "default":
            return HTTPStatusPattern(pattern=pattern, code_range=None)

        if pattern.endswith("XX") and pattern[0].isdigit():
            first_digit = int(pattern[0])
            return HTTPStatusPattern(pattern=pattern, code_range=(first_digit * 100, first_digit * 100 + 99))

        try:
            code = int(pattern)
            return HTTPStatusPattern(pattern=pattern, code_range=(code, code))
        except ValueError:
            return ParseError(
                detail=(
                    f"Invalid response status code pattern: {pattern}, response will be omitted from generated client"
                )
            )

    def is_range(self) -> bool:
        """Check if this is a range of status codes, such as 2XX"""
        return self.range is not None and self.range[0] != self.range[1]

    def __lt__(self, other: "HTTPStatusPattern") -> bool:
        """Compare two HTTPStatusPattern objects based on the order they should be applied in"""
        if self.range is None:
            return False  # Default gets applied last
        if other.range is None:
            return True  # Other is default, so this one gets applied first

        # Specific codes appear before ranges
        if self.is_range() and not other.is_range():
            return False
        if not self.is_range() and other.is_range():
            return True

        # Order specific codes numerically
        return self.range[0] < other.range[0]

    def __eq__(self, other: object) -> bool:  # pragma: no cover
        if not isinstance(other, HTTPStatusPattern):
            return False
        return self.range == other.range

    def __hash__(self) -> int:  # pragma: no cover
        return hash(self.range)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<HTTPStatusPattern {self.pattern}>"


@define(order=False)
class Response:
    """Describes a single response for an endpoint"""

    status_code: HTTPStatusPattern
    prop: Property
    source: _ResponseSource
    data: oai.Response | oai.Reference  # Original data which created this response, useful for custom templates

    def is_default(self) -> bool:
        return self.status_code.range is None

    def __lt__(self, other: "Response") -> bool:
        """Compare two responses based on the order in which they should be applied in"""
        return self.status_code < other.status_code


def _source_by_content_type(content_type: str, config: Config) -> _ResponseSource | None:
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
    status_code: HTTPStatusPattern,
    response_name: str,
    config: Config,
    data: oai.Response | oai.Reference,
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


def response_from_data(  # noqa: PLR0911
    *,
    status_code: HTTPStatusPattern,
    data: oai.Response | oai.Reference,
    schemas: Schemas,
    responses: dict[str, oai.Response | oai.Reference],
    parent_name: str,
    config: Config,
) -> tuple[Response | ParseError, Schemas]:
    """Generate a Response from the OpenAPI dictionary representation of it"""

    response_name = f"response_{status_code.pattern}"
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
