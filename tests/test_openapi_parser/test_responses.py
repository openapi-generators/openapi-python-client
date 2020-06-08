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

        assert (
            r.constructor()
            == "[SuperCoolClass.from_dict(item) for item in cast(List[Dict[str, Any]], response.json())]"
        )


class TestRefResponse:
    def test_return_string(self, mocker):
        from openapi_python_client.openapi_parser.responses import RefResponse

        r = RefResponse(200, reference=mocker.MagicMock(class_name="SuperCoolClass"))

        assert r.return_string() == "SuperCoolClass"

    def test_constructor(self, mocker):
        from openapi_python_client.openapi_parser.responses import RefResponse

        r = RefResponse(200, reference=mocker.MagicMock(class_name="SuperCoolClass"))

        assert r.constructor() == "SuperCoolClass.from_dict(cast(Dict[str, Any], response.json()))"


class TestBasicResponse:
    def test_return_string(self):
        from openapi_python_client.openapi_parser.responses import BasicResponse

        r = BasicResponse(200, "string")

        assert r.return_string() == "str"

        r = BasicResponse(200, "number")

        assert r.return_string() == "float"

        r = BasicResponse(200, "integer")

        assert r.return_string() == "int"

        r = BasicResponse(200, "boolean")

        assert r.return_string() == "bool"

    def test_constructor(self):
        from openapi_python_client.openapi_parser.responses import BasicResponse

        r = BasicResponse(200, "string")

        assert r.constructor() == "str(response.text)"

        r = BasicResponse(200, "number")

        assert r.constructor() == "float(response.text)"

        r = BasicResponse(200, "integer")

        assert r.constructor() == "int(response.text)"

        r = BasicResponse(200, "boolean")

        assert r.constructor() == "bool(response.text)"


class TestResponseFromDict:
    def test_response_from_dict_no_content(self, mocker):
        from openapi_python_client.openapi_parser.responses import response_from_dict
        Response = mocker.patch(f"{MODULE_NAME}.Response")

        status_code = mocker.MagicMock(autospec=int)
        response = response_from_dict(status_code=status_code, data={}) 
        
        Response.assert_called_once_with(status_code=status_code)
        assert response == Response()

    def test_response_from_dict_unsupported_content_type(self):
        from openapi_python_client.openapi_parser.responses import response_from_dict

        with pytest.raises(ValueError):
            response_from_dict(status_code=200, data={"content": {"not/real": {}}})

    def test_response_from_dict_ref(self, mocker):
        ref = mocker.MagicMock()
        status_code = mocker.MagicMock(autospec=int)
        data = {"content": {"application/json": {"schema": {"$ref": ref}}}}
        from_ref = mocker.patch(f"{MODULE_NAME}.Reference.from_ref")
        RefResponse = mocker.patch(f"{MODULE_NAME}.RefResponse")
        from openapi_python_client.openapi_parser.responses import response_from_dict

        response = response_from_dict(status_code=status_code, data=data)

        from_ref.assert_called_once_with(ref)
        RefResponse.assert_called_once_with(status_code=status_code, reference=from_ref())
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
        from_ref = mocker.patch(f"{MODULE_NAME}.Reference.from_ref")
        ListRefResponse = mocker.patch(f"{MODULE_NAME}.ListRefResponse")
        from openapi_python_client.openapi_parser.responses import response_from_dict

        response = response_from_dict(status_code=status_code, data=data)

        from_ref.assert_called_once_with(ref)
        ListRefResponse.assert_called_once_with(status_code=status_code, reference=from_ref())
        assert response == ListRefResponse()

    def test_response_from_dict_basic(self, mocker):
        status_code = mocker.MagicMock(autospec=int)
        data = {"content": {"text/html": {"schema": {"type": "string"}}}}
        BasicResponse = mocker.patch(f"{MODULE_NAME}.BasicResponse")
        from openapi_python_client.openapi_parser.responses import response_from_dict

        response = response_from_dict(status_code=status_code, data=data)

        BasicResponse.assert_called_once_with(status_code=status_code, openapi_type="string")
        assert response == BasicResponse.return_value

    def test_response_from_dict_unsupported_type(self):
        from openapi_python_client.openapi_parser.responses import response_from_dict

        with pytest.raises(ValueError):
            response_from_dict(status_code=200, data={"content": {"application/json": {"schema": {"type": "blah"}}}})
