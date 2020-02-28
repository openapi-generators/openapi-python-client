import pytest

MODULE_NAME = "openapi_python_client.openapi_parser.responses"


class TestResponse:
    def test_return_string(self):
        from openapi_python_client.openapi_parser.responses import Response

        r = Response(200)

        assert r.return_string() == "None"

    def test_constructor(self):
        from openapi_python_client.openapi_parser.responses import Response

        r = Response(200)

        assert r.constructor() == "None"


class TestListRefResponse:
    def test_return_string(self, mocker):
        from openapi_python_client.openapi_parser.responses import ListRefResponse

        r = ListRefResponse(200, reference=mocker.MagicMock(class_name="SuperCoolClass"))

        assert r.return_string() == "List[SuperCoolClass]"

    def test_constructor(self, mocker):
        from openapi_python_client.openapi_parser.responses import ListRefResponse

        r = ListRefResponse(200, reference=mocker.MagicMock(class_name="SuperCoolClass"))

        assert r.constructor() == "[SuperCoolClass.from_dict(item) for item in response.json()]"


class TestStringResponse:
    def test_return_string(self):
        from openapi_python_client.openapi_parser.responses import StringResponse

        r = StringResponse(200)

        assert r.return_string() == "str"

    def test_constructor(self):
        from openapi_python_client.openapi_parser.responses import StringResponse

        r = StringResponse(200)

        assert r.constructor() == "response.text"


class TestResponseFromDict:
    def test_response_from_dict_no_content(self):
        from openapi_python_client.openapi_parser.responses import response_from_dict

        with pytest.raises(ValueError):
            response_from_dict(status_code=200, data={})

    def test_response_from_dict_unsupported_content_type(self):
        from openapi_python_client.openapi_parser.responses import response_from_dict

        with pytest.raises(ValueError):
            response_from_dict(status_code=200, data={"content": {"not/real": {}}})

    def test_response_from_dict_ref(self, mocker):
        ref = mocker.MagicMock()
        status_code = mocker.MagicMock(autospec=int)
        data = {"content": {"application/json": {"schema": {"$ref": ref}}}}
        Reference = mocker.patch(f"{MODULE_NAME}.Reference")
        RefResponse = mocker.patch(f"{MODULE_NAME}.RefResponse")
        from openapi_python_client.openapi_parser.responses import response_from_dict

        response = response_from_dict(status_code=status_code, data=data)

        Reference.assert_called_once_with(ref)
        RefResponse.assert_called_once_with(status_code=status_code, reference=Reference())
        assert response == RefResponse()

    def test_response_from_dict_empty(self, mocker):
        status_code = mocker.MagicMock(autospec=int)
        data = {"content": {"application/json": {"schema": {}}}}
        Response = mocker.patch(f"{MODULE_NAME}.Response")
        from openapi_python_client.openapi_parser.responses import response_from_dict

        response = response_from_dict(status_code=status_code, data=data)

        Response.assert_called_once_with(status_code=status_code)
        assert response == Response()

    def test_response_from_dict_array(self, mocker):
        ref = mocker.MagicMock()
        status_code = mocker.MagicMock(autospec=int)
        data = {"content": {"application/json": {"schema": {"type": "array", "items": {"$ref": ref}}}}}
        Reference = mocker.patch(f"{MODULE_NAME}.Reference")
        ListRefResponse = mocker.patch(f"{MODULE_NAME}.ListRefResponse")
        from openapi_python_client.openapi_parser.responses import response_from_dict

        response = response_from_dict(status_code=status_code, data=data)

        Reference.assert_called_once_with(ref)
        ListRefResponse.assert_called_once_with(status_code=status_code, reference=Reference())
        assert response == ListRefResponse()

    def test_response_from_dict_string(self, mocker):
        status_code = mocker.MagicMock(autospec=int)
        data = {"content": {"text/html": {"schema": {"type": "string"}}}}
        StringResponse = mocker.patch(f"{MODULE_NAME}.StringResponse")
        from openapi_python_client.openapi_parser.responses import response_from_dict

        response = response_from_dict(status_code=status_code, data=data)

        StringResponse.assert_called_once_with(status_code=status_code)
        assert response == StringResponse()

    def test_response_from_dict_unsupported_type(self):
        from openapi_python_client.openapi_parser.responses import response_from_dict

        with pytest.raises(ValueError):
            response_from_dict(status_code=200, data={"content": {"application/json": {"schema": {"type": "blah"}}}})
