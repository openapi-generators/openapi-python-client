from unittest.mock import MagicMock

import openapi_python_client.schema as oai
from openapi_python_client.parser.errors import ParseError, PropertyError
from openapi_python_client.parser.properties import AnyProperty, Schemas, StringProperty

MODULE_NAME = "openapi_python_client.parser.responses"


def test_response_from_data_no_content():
    from openapi_python_client.parser.responses import Response, response_from_data

    response, schemas = response_from_data(
        status_code=200,
        data=oai.Response.construct(description=""),
        schemas=Schemas(),
        parent_name="parent",
        config=MagicMock(),
    )

    assert response == Response(
        status_code=200,
        prop=AnyProperty(
            name="response_200",
            default=None,
            nullable=False,
            required=True,
            python_name="response_200",
            description="",
            example="",
        ),
        source="None",
    )


def test_response_from_data_unsupported_content_type():
    from openapi_python_client.parser.responses import response_from_data

    data = oai.Response.construct(description="", content={"blah": None})
    response, schemas = response_from_data(
        status_code=200, data=data, schemas=Schemas(), parent_name="parent", config=MagicMock()
    )

    assert response == ParseError(data=data, detail="Unsupported content_type {'blah': None}")


def test_response_from_data_no_content_schema():
    from openapi_python_client.parser.responses import Response, response_from_data

    data = oai.Response.construct(description="", content={"application/json": oai.MediaType.construct()})
    response, schemas = response_from_data(
        status_code=200, data=data, schemas=Schemas(), parent_name="parent", config=MagicMock()
    )

    assert response == Response(
        status_code=200,
        prop=AnyProperty(
            name="response_200",
            default=None,
            nullable=False,
            required=True,
            python_name="response_200",
            description=data.description,
            example=data.example,
        ),
        source="None",
    )


def test_response_from_data_property_error(mocker):
    from openapi_python_client.parser import responses

    property_from_data = mocker.patch.object(responses, "property_from_data", return_value=(PropertyError(), Schemas()))
    data = oai.Response.construct(
        description="", content={"application/json": oai.MediaType.construct(media_type_schema="something")}
    )
    config = MagicMock()

    response, schemas = responses.response_from_data(
        status_code=400, data=data, schemas=Schemas(), parent_name="parent", config=config
    )

    assert response == PropertyError()
    property_from_data.assert_called_once_with(
        name="response_400", required=True, data="something", schemas=Schemas(), parent_name="parent", config=config
    )


def test_response_from_data_property(mocker, property_factory):
    from openapi_python_client.parser import responses

    prop = property_factory()
    property_from_data = mocker.patch.object(responses, "property_from_data", return_value=(prop, Schemas()))
    data = oai.Response.construct(
        description="", content={"application/json": oai.MediaType.construct(media_type_schema="something")}
    )
    config = MagicMock()

    response, schemas = responses.response_from_data(
        status_code=400, data=data, schemas=Schemas(), parent_name="parent", config=config
    )

    assert response == responses.Response(
        status_code=400,
        prop=prop,
        source="response.json()",
    )
    property_from_data.assert_called_once_with(
        name="response_400", required=True, data="something", schemas=Schemas(), parent_name="parent", config=config
    )
