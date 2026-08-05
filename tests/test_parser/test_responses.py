from unittest.mock import MagicMock

import pytest

import openapi_python_client.schema as oai
from openapi_python_client.parser import responses
from openapi_python_client.parser.errors import ParseError, PropertyError
from openapi_python_client.parser.properties import Schemas
from openapi_python_client.parser.responses import (
    BYTES_SOURCE,
    JSON_SOURCE,
    NONE_SOURCE,
    TEXT_SOURCE,
    HTTPStatusPattern,
    Response,
    _ResponseSource,
    response_from_data,
)

MODULE_NAME = "openapi_python_client.parser.responses"


def test_response_from_data_no_content(any_property_factory):
    data = oai.Response.model_construct(description="")

    response, _schemas = response_from_data(
        status_code=HTTPStatusPattern(pattern="200", code_range=(200, 200)),
        data=data,
        schemas=Schemas(),
        responses={},
        parent_name="parent",
        config=MagicMock(),
    )

    assert response == Response(
        status_code=HTTPStatusPattern(pattern="200", code_range=(200, 200)),
        prop=any_property_factory(
            name="response_200",
            default=None,
            required=True,
            description="",
        ),
        source=NONE_SOURCE,
        data=data,
    )


status_code = HTTPStatusPattern(pattern="200", code_range=(200, 200))


def test_response_from_data_unsupported_content_type():
    data = oai.Response.model_construct(description="", content={"blah": None})
    config = MagicMock()
    config.content_type_overrides = {}
    response, _schemas = response_from_data(
        status_code=status_code,
        data=data,
        schemas=Schemas(),
        responses={},
        parent_name="parent",
        config=config,
    )

    assert response == ParseError(data=data, detail="Unsupported content_type {'blah': None}")


def test_response_from_data_no_content_schema(any_property_factory):
    data = oai.Response.model_construct(
        description="",
        content={"application/vnd.api+json; version=2.2": oai.MediaType.model_construct()},
    )
    config = MagicMock()
    config.content_type_overrides = {}
    response, _schemas = response_from_data(
        status_code=status_code,
        data=data,
        schemas=Schemas(),
        responses={},
        parent_name="parent",
        config=config,
    )

    assert response == Response(
        status_code=status_code,
        prop=any_property_factory(
            name="response_200",
            default=None,
            required=True,
            description=data.description,
        ),
        source=NONE_SOURCE,
        data=data,
    )


def test_response_from_data_property_error(mocker):
    property_from_data = mocker.patch.object(responses, "property_from_data", return_value=(PropertyError(), Schemas()))
    data = oai.Response.model_construct(
        description="",
        content={"application/json": oai.MediaType.model_construct(media_type_schema="something")},
    )
    config = MagicMock()
    config.content_type_overrides = {}

    response, _schemas = responses.response_from_data(
        status_code=HTTPStatusPattern(pattern="400", code_range=(400, 400)),
        data=data,
        schemas=Schemas(),
        responses={},
        parent_name="parent",
        config=config,
    )

    assert response == PropertyError()
    property_from_data.assert_called_once_with(
        name="response_400",
        required=True,
        data="something",
        schemas=Schemas(),
        parent_name="parent",
        config=config,
    )


def test_response_from_data_property(mocker, any_property_factory):
    prop = any_property_factory()
    property_from_data = mocker.patch.object(responses, "property_from_data", return_value=(prop, Schemas()))
    data = oai.Response.model_construct(
        description="",
        content={"application/json": oai.MediaType.model_construct(media_type_schema="something")},
    )
    config = MagicMock()
    config.content_type_overrides = {}
    status_code = HTTPStatusPattern(pattern="400", code_range=(400, 400))

    response, _schemas = responses.response_from_data(
        status_code=status_code,
        data=data,
        schemas=Schemas(),
        responses={},
        parent_name="parent",
        config=config,
    )

    assert response == responses.Response(
        status_code=status_code,
        prop=prop,
        source=JSON_SOURCE,
        data=data,
    )
    property_from_data.assert_called_once_with(
        name="response_400",
        required=True,
        data="something",
        schemas=Schemas(),
        parent_name="parent",
        config=config,
    )


def test_response_from_data_reference(mocker, any_property_factory):
    prop = any_property_factory()
    mocker.patch.object(responses, "property_from_data", return_value=(prop, Schemas()))
    predefined_response_data = oai.Response.model_construct(
        description="",
        content={"application/json": oai.MediaType.model_construct(media_type_schema="something")},
    )
    config = MagicMock()
    config.content_type_overrides = {}

    response, _schemas = responses.response_from_data(
        status_code=HTTPStatusPattern(pattern="400", code_range=(400, 400)),
        data=oai.Reference.model_construct(ref="#/components/responses/ErrorResponse"),
        schemas=Schemas(),
        responses={"ErrorResponse": predefined_response_data},
        parent_name="parent",
        config=config,
    )

    assert response == responses.Response(
        status_code=HTTPStatusPattern(pattern="400", code_range=(400, 400)),
        prop=prop,
        source=JSON_SOURCE,
        data=predefined_response_data,
    )


@pytest.mark.parametrize(
    "ref_string,expected_error_string",
    [
        ("#/components/responses/Nonexistent", "Could not find"),
        ("https://remote-reference", "Remote references"),
        ("#/components/something-that-isnt-responses/ErrorResponse", "not allowed in responses"),
    ],
)
def test_response_from_data_invalid_reference(ref_string, expected_error_string, mocker, any_property_factory):
    prop = any_property_factory()
    mocker.patch.object(responses, "property_from_data", return_value=(prop, Schemas()))
    predefined_response_data = oai.Response.model_construct(
        description="",
        content={"application/json": oai.MediaType.model_construct(media_type_schema="something")},
    )
    config = MagicMock()
    config.content_type_overrides = {}

    response, _schemas = responses.response_from_data(
        status_code=HTTPStatusPattern(pattern="400", code_range=(400, 400)),
        data=oai.Reference.model_construct(ref=ref_string),
        schemas=Schemas(),
        responses={"ErrorResponse": predefined_response_data},
        parent_name="parent",
        config=config,
    )

    assert isinstance(response, ParseError)
    assert expected_error_string in response.detail


def test_response_from_data_ref_to_response_that_is_a_ref(mocker, any_property_factory):
    prop = any_property_factory()
    mocker.patch.object(responses, "property_from_data", return_value=(prop, Schemas()))
    predefined_response_base_data = oai.Response.model_construct(
        description="",
        content={"application/json": oai.MediaType.model_construct(media_type_schema="something")},
    )
    predefined_response_data = oai.Reference.model_construct(
        ref="#/components/references/BaseResponse",
    )
    config = MagicMock()
    config.content_type_overrides = {}

    response, _schemas = responses.response_from_data(
        status_code=HTTPStatusPattern(pattern="400", code_range=(400, 400)),
        data=oai.Reference.model_construct(ref="#/components/responses/ErrorResponse"),
        schemas=Schemas(),
        responses={
            "BaseResponse": predefined_response_base_data,
            "ErrorResponse": predefined_response_data,
        },
        parent_name="parent",
        config=config,
    )

    assert isinstance(response, ParseError)
    assert response.detail is not None and "Top-level $ref" in response.detail


def test_response_from_data_content_type_overrides(any_property_factory):
    data = oai.Response.model_construct(
        description="",
        content={"application/zip": oai.MediaType.model_construct()},
    )
    config = MagicMock()
    config.content_type_overrides = {"application/zip": "application/octet-stream"}
    response, _schemas = response_from_data(
        status_code=HTTPStatusPattern(pattern="200", code_range=(200, 200)),
        data=data,
        schemas=Schemas(),
        responses={},
        parent_name="parent",
        config=config,
    )

    assert response == Response(
        status_code=HTTPStatusPattern(pattern="200", code_range=(200, 200)),
        prop=any_property_factory(
            name="response_200",
            default=None,
            required=True,
            description=data.description,
        ),
        source=NONE_SOURCE,
        data=data,
    )


@pytest.mark.parametrize(
    "pattern1, pattern2, result",
    [
        ("400", "401", True),
        ("503", "500", False),
        ("default", "400", False),
        ("400", "default", True),
        ("2XX", "3XX", True),
        ("3XX", "2XX", False),
        ("2XX", "400", False),
    ],
)
def test_http_status_pattern_lt(pattern1: str, pattern2: str, result: bool) -> None:
    first = HTTPStatusPattern.parse(pattern1)
    second = HTTPStatusPattern.parse(pattern2)
    assert isinstance(first, HTTPStatusPattern)
    assert isinstance(second, HTTPStatusPattern)
    assert (first < second) == result


@pytest.mark.parametrize(
    "pattern, expected",
    [
        ("200", True),
        ("204", True),
        ("299", True),
        ("2XX", True),
        # `default` is the catch-all for unmatched statuses and stays on the return path, so it is not a success
        # pattern; 1XX and 3XX have no value to hand back, so they are raised rather than returned.
        ("default", False),
        ("1XX", False),
        ("3XX", False),
        ("400", False),
        ("404", False),
        ("4XX", False),
        ("500", False),
    ],
)
def test_http_status_pattern_is_success(pattern: str, expected: bool) -> None:
    parsed = HTTPStatusPattern.parse(pattern)
    assert isinstance(parsed, HTTPStatusPattern)
    assert parsed.is_success() is expected


@pytest.mark.parametrize("pattern, expected", [("200", True), ("422", False)])
def test_response_is_success_delegates_to_its_pattern(pattern, expected, any_property_factory) -> None:
    response = Response(
        status_code=HTTPStatusPattern.parse(pattern),
        prop=any_property_factory(name=f"response_{pattern}"),
        source=JSON_SOURCE,
        data=oai.Response.model_construct(description=""),
    )

    assert response.is_success() is expected


def test_response_has_content(any_property_factory) -> None:
    data = oai.Response.model_construct(description="")
    prop = any_property_factory(name="response_200")

    assert Response(status_code=status_code, prop=prop, source=JSON_SOURCE, data=data).has_content() is True
    assert Response(status_code=status_code, prop=prop, source=NONE_SOURCE, data=data).has_content() is False


def test_response_source_can_fail(any_property_factory) -> None:
    """The text and bytes sources are plain attribute reads; anything else is assumed able to raise."""
    data = oai.Response.model_construct(description="")
    prop = any_property_factory(name="response_200")

    def source_can_fail(source) -> bool:
        return Response(status_code=status_code, prop=prop, source=source, data=data).source_can_fail()

    assert source_can_fail(TEXT_SOURCE) is False
    assert source_can_fail(BYTES_SOURCE) is False
    # Unreachable at the only call site, which `has_content()` already gates on this exact value, but the answer
    # for a literal `None` read is still False.
    assert source_can_fail(NONE_SOURCE) is False
    assert source_can_fail(JSON_SOURCE) is True
    # A source nobody has vetted defaults to guarded rather than to unguarded.
    assert source_can_fail(_ResponseSource(attribute="response.something_new()", return_type="Any")) is True


@pytest.mark.parametrize(
    "content",
    [
        pytest.param(None, id="no content at all"),
        pytest.param({"application/json": oai.MediaType.model_construct()}, id="content with no schema"),
    ],
)
def test_response_from_data_without_a_body_has_no_content(content) -> None:
    """Both shapes go through `empty_response`, so neither can supply `UnexpectedStatus(parsed=...)`."""
    config = MagicMock()
    config.content_type_overrides = {}

    response, _schemas = response_from_data(
        status_code=HTTPStatusPattern.parse("404"),
        data=oai.Response.model_construct(description="", content=content),
        schemas=Schemas(),
        responses={},
        parent_name="parent",
        config=config,
    )

    assert isinstance(response, Response)
    assert response.has_content() is False
