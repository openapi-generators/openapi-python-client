from unittest.mock import MagicMock

import pytest

import openapi_python_client.schema as oai
from openapi_python_client.parser import responses
from openapi_python_client.parser.errors import ParseError, PropertyError
from openapi_python_client.parser.properties import Schemas
from openapi_python_client.parser.responses import (
    JSON_SOURCE,
    NONE_SOURCE,
    HTTPStatusPattern,
    Response,
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
