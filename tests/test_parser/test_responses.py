from unittest.mock import MagicMock

import pytest

import openapi_python_client.schema as oai
from openapi_python_client.parser.errors import ParseError, PropertyError
from openapi_python_client.parser.properties import Schemas
from openapi_python_client.parser.responses import JSON_SOURCE, NONE_SOURCE

MODULE_NAME = "openapi_python_client.parser.responses"


def test_response_from_data_no_content(any_property_factory):
    from openapi_python_client.parser.responses import Response, response_from_data

    data = oai.Response.model_construct(description="")

    response, schemas = response_from_data(
        status_code=200,
        data=data,
        schemas=Schemas(),
        responses={},
        parent_name="parent",
        config=MagicMock(),
    )

    assert response == Response(
        status_code=200,
        prop=any_property_factory(
            name="response_200",
            default=None,
            required=True,
            description="",
        ),
        source=NONE_SOURCE,
        data=data,
    )


def test_response_from_data_unsupported_content_type():
    from openapi_python_client.parser.responses import response_from_data

    data = oai.Response.model_construct(description="", content={"blah": None})
    config = MagicMock()
    config.content_type_overrides = {}
    response, schemas = response_from_data(
        status_code=200,
        data=data,
        schemas=Schemas(),
        responses={},
        parent_name="parent",
        config=config,
    )

    assert response == ParseError(data=data, detail="Unsupported content_type {'blah': None}")


def test_response_from_data_no_content_schema(any_property_factory):
    from openapi_python_client.parser.responses import Response, response_from_data

    data = oai.Response.model_construct(
        description="",
        content={"application/vnd.api+json; version=2.2": oai.MediaType.model_construct()},
    )
    config = MagicMock()
    config.content_type_overrides = {}
    response, schemas = response_from_data(
        status_code=200,
        data=data,
        schemas=Schemas(),
        responses={},
        parent_name="parent",
        config=config,
    )

    assert response == Response(
        status_code=200,
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
    from openapi_python_client.parser import responses

    property_from_data = mocker.patch.object(responses, "property_from_data", return_value=(PropertyError(), Schemas()))
    data = oai.Response.model_construct(
        description="",
        content={"application/json": oai.MediaType.model_construct(media_type_schema="something")},
    )
    config = MagicMock()
    config.content_type_overrides = {}

    response, schemas = responses.response_from_data(
        status_code=400,
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
    from openapi_python_client.parser import responses

    prop = any_property_factory()
    property_from_data = mocker.patch.object(responses, "property_from_data", return_value=(prop, Schemas()))
    data = oai.Response.model_construct(
        description="",
        content={"application/json": oai.MediaType.model_construct(media_type_schema="something")},
    )
    config = MagicMock()
    config.content_type_overrides = {}

    response, schemas = responses.response_from_data(
        status_code=400,
        data=data,
        schemas=Schemas(),
        responses={},
        parent_name="parent",
        config=config,
    )

    assert response == responses.Response(
        status_code=400,
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
    from openapi_python_client.parser import responses

    prop = any_property_factory()
    mocker.patch.object(responses, "property_from_data", return_value=(prop, Schemas()))
    predefined_response_data = oai.Response.model_construct(
        description="",
        content={"application/json": oai.MediaType.model_construct(media_type_schema="something")},
    )
    config = MagicMock()
    config.content_type_overrides = {}

    response, schemas = responses.response_from_data(
        status_code=400,
        data=oai.Reference.model_construct(ref="#/components/responses/ErrorResponse"),
        schemas=Schemas(),
        responses={"ErrorResponse": predefined_response_data},
        parent_name="parent",
        config=config,
    )

    assert response == responses.Response(
        status_code=400,
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
    from openapi_python_client.parser import responses

    prop = any_property_factory()
    mocker.patch.object(responses, "property_from_data", return_value=(prop, Schemas()))
    predefined_response_data = oai.Response.model_construct(
        description="",
        content={"application/json": oai.MediaType.model_construct(media_type_schema="something")},
    )
    config = MagicMock()
    config.content_type_overrides = {}

    response, schemas = responses.response_from_data(
        status_code=400,
        data=oai.Reference.model_construct(ref=ref_string),
        schemas=Schemas(),
        responses={"ErrorResponse": predefined_response_data},
        parent_name="parent",
        config=config,
    )

    assert isinstance(response, ParseError)
    assert expected_error_string in response.detail


def test_response_from_data_ref_to_response_that_is_a_ref(mocker, any_property_factory):
    from openapi_python_client.parser import responses

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

    response, schemas = responses.response_from_data(
        status_code=400,
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
    assert "Top-level $ref" in response.detail


def test_response_from_data_content_type_overrides(any_property_factory):
    from openapi_python_client.parser.responses import Response, response_from_data

    data = oai.Response.model_construct(
        description="",
        content={"application/zip": oai.MediaType.model_construct()},
    )
    config = MagicMock()
    config.content_type_overrides = {"application/zip": "application/octet-stream"}
    response, schemas = response_from_data(
        status_code=200,
        data=data,
        schemas=Schemas(),
        responses={},
        parent_name="parent",
        config=config,
    )

    assert response == Response(
        status_code=200,
        prop=any_property_factory(
            name="response_200",
            default=None,
            required=True,
            description=data.description,
        ),
        source=NONE_SOURCE,
        data=data,
    )
