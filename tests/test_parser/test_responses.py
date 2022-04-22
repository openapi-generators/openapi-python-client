import openapi_python_client.schema as oai
from openapi_python_client.parser.errors import ParseError, PropertyError
from openapi_python_client.parser.properties import NoneProperty, Schemas, StringProperty

MODULE_NAME = "openapi_python_client.parser.responses"


def test_response_from_data_no_content():
    from openapi_python_client.parser.responses import Response, response_from_data

    response, schemas = response_from_data(
        status_code=200, data=oai.Response.construct(description="description"), schemas=Schemas(), parent_name="parent"
    )

    assert response == Response(
        status_code=200,
        prop=NoneProperty(name="response_200", default=None, nullable=False, required=True, description=None),
        source="None",
    )


def test_response_from_data_unsupported_content_type():
    from openapi_python_client.parser.responses import response_from_data

    data = oai.Response.construct(description="description", content={"blah": None})
    response, schemas = response_from_data(status_code=200, data=data, schemas=Schemas(), parent_name="parent")

    assert response == ParseError(data=data, detail="Unsupported content_type {'blah': None}")


def test_response_from_data_no_content_schema():
    from openapi_python_client.parser.responses import Response, response_from_data

    data = oai.Response.construct(description="", content={"application/json": oai.MediaType.construct()})
    response, schemas = response_from_data(status_code=200, data=data, schemas=Schemas(), parent_name="parent")
    assert response == Response(
        status_code=200,
        prop=NoneProperty(name="response_200", default=None, nullable=False, required=True, description=None),
        source="None",
    )


def test_response_from_data_property_error(mocker):
    from openapi_python_client.parser import responses

    property_from_data = mocker.patch.object(responses, "property_from_data", return_value=(PropertyError(), Schemas()))
    data = oai.Response.construct(
        description="description", content={"application/json": oai.MediaType.construct(media_type_schema="something")}
    )
    response, schemas = responses.response_from_data(
        status_code=400, data=data, schemas=Schemas(), parent_name="parent"
    )

    assert response == PropertyError()
    property_from_data.assert_called_once_with(
        name="response_400", required=True, data="something", schemas=Schemas(), parent_name="parent"
    )


def test_response_from_data_property(mocker):
    from openapi_python_client.parser import responses

    prop = StringProperty(name="prop", required=True, nullable=False, default=None, description=None)
    property_from_data = mocker.patch.object(responses, "property_from_data", return_value=(prop, Schemas()))
    data = oai.Response.construct(
        description="", content={"application/json": oai.MediaType.construct(media_type_schema="something")}
    )
    response, schemas = responses.response_from_data(
        status_code=400, data=data, schemas=Schemas(), parent_name="parent"
    )

    assert response == responses.Response(
        status_code=400,
        prop=prop,
        source="response.json()",
    )
    property_from_data.assert_called_once_with(
        name="response_400", required=True, data="something", schemas=Schemas(), parent_name="parent"
    )


def test_response_from_data_property_of_type_text_yaml(mocker):
    from openapi_python_client.parser import responses

    prop = StringProperty(name="prop", required=True, nullable=False, default=None, description=None)
    property_from_data = mocker.patch.object(responses, "property_from_data", return_value=(prop, Schemas()))
    data = oai.Response.construct(
        description="", content={"text/yaml": oai.MediaType.construct(media_type_schema="something")}
    )
    response, schemas = responses.response_from_data(
        status_code=400, data=data, schemas=Schemas(), parent_name="parent"
    )

    assert response == responses.Response(
        status_code=400,
        prop=prop,
        source="response.yaml",
    )
    property_from_data.assert_called_once_with(
        name="response_400", required=True, data="something", schemas=Schemas(), parent_name="parent"
    )
