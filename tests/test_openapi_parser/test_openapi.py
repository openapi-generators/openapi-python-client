import pytest

MODULE_NAME = "openapi_python_client.openapi_parser.openapi"


class TestOpenAPI:
    def test_from_dict(self, mocker):
        Schema = mocker.patch(f"{MODULE_NAME}.Schema")
        schemas = mocker.MagicMock()
        Schema.dict.return_value = schemas
        EndpointCollection = mocker.patch(f"{MODULE_NAME}.EndpointCollection")
        endpoint_collections_by_tag = mocker.MagicMock()
        EndpointCollection.from_dict.return_value = endpoint_collections_by_tag
        in_dict = {
            "components": {"schemas": mocker.MagicMock()},
            "paths": mocker.MagicMock(),
            "info": {"title": mocker.MagicMock(), "description": mocker.MagicMock(), "version": mocker.MagicMock()},
        }
        get_all_enums = mocker.patch(f"{MODULE_NAME}.EnumProperty.get_all_enums")

        from openapi_python_client.openapi_parser.openapi import OpenAPI

        openapi = OpenAPI.from_dict(in_dict)

        Schema.dict.assert_called_once_with(in_dict["components"]["schemas"])
        EndpointCollection.from_dict.assert_called_once_with(in_dict["paths"])
        get_all_enums.assert_called_once_with()
        assert openapi == OpenAPI(
            title=in_dict["info"]["title"],
            description=in_dict["info"]["description"],
            version=in_dict["info"]["version"],
            endpoint_collections_by_tag=endpoint_collections_by_tag,
            schemas=schemas,
            enums=get_all_enums.return_value,
        )


class TestSchema:
    def test_dict(self, mocker):
        from_dict = mocker.patch(f"{MODULE_NAME}.Schema.from_dict")
        in_data = {1: mocker.MagicMock(), 2: mocker.MagicMock()}
        schema_1 = mocker.MagicMock()
        schema_2 = mocker.MagicMock()
        from_dict.side_effect = [schema_1, schema_2]

        from openapi_python_client.openapi_parser.openapi import Schema

        result = Schema.dict(in_data)

        from_dict.assert_has_calls([mocker.call(value, name=name) for (name, value) in in_data.items()])
        assert result == {
            schema_1.reference.class_name: schema_1,
            schema_2.reference.class_name: schema_2,
        }

    def test_from_dict(self, mocker):
        from openapi_python_client.openapi_parser.properties import Property

        in_data = {
            "title": mocker.MagicMock(),
            "description": mocker.MagicMock(),
            "required": ["RequiredEnum"],
            "properties": {"RequiredEnum": mocker.MagicMock(), "OptionalDateTime": mocker.MagicMock(),},
        }
        required_property = mocker.MagicMock(autospec=Property)
        required_imports = mocker.MagicMock()
        required_property.get_imports.return_value = {required_imports}
        optional_property = mocker.MagicMock(autospec=Property)
        optional_imports = mocker.MagicMock()
        optional_property.get_imports.return_value = {optional_imports}
        property_from_dict = mocker.patch(
            f"{MODULE_NAME}.property_from_dict", side_effect=[required_property, optional_property],
        )
        from_ref = mocker.patch(f"{MODULE_NAME}.Reference.from_ref")

        from openapi_python_client.openapi_parser.openapi import Schema

        result = Schema.from_dict(in_data, name=mocker.MagicMock())

        from_ref.assert_called_once_with(in_data["title"])
        property_from_dict.assert_has_calls(
            [
                mocker.call(name="RequiredEnum", required=True, data=in_data["properties"]["RequiredEnum"]),
                mocker.call(name="OptionalDateTime", required=False, data=in_data["properties"]["OptionalDateTime"]),
            ]
        )
        required_property.get_imports.assert_called_once_with(prefix="")
        optional_property.get_imports.assert_called_once_with(prefix="")
        assert result == Schema(
            reference=from_ref(),
            required_properties=[required_property],
            optional_properties=[optional_property],
            relative_imports={required_imports, optional_imports,},
            description=in_data["description"],
        )


class TestEndpoint:
    def test_parse_request_form_body(self, mocker):
        ref = mocker.MagicMock()
        body = {"content": {"application/x-www-form-urlencoded": {"schema": {"$ref": ref}}}}
        from_ref = mocker.patch(f"{MODULE_NAME}.Reference.from_ref")

        from openapi_python_client.openapi_parser.openapi import Endpoint

        result = Endpoint.parse_request_form_body(body)

        from_ref.assert_called_once_with(ref)
        assert result == from_ref()

    def test_parse_request_form_body_no_data(self):
        body = {"content": {}}

        from openapi_python_client.openapi_parser.openapi import Endpoint

        result = Endpoint.parse_request_form_body(body)

        assert result is None

    def test_parse_multipart_body(self, mocker):
        ref = mocker.MagicMock()
        body = {"content": {"multipart/form-data": {"schema": {"$ref": ref}}}}
        from_ref = mocker.patch(f"{MODULE_NAME}.Reference.from_ref")

        from openapi_python_client.openapi_parser.openapi import Endpoint

        result = Endpoint.parse_multipart_body(body)

        from_ref.assert_called_once_with(ref)
        assert result == from_ref()

    def test_parse_multipart_body_no_data(self):
        body = {"content": {}}

        from openapi_python_client.openapi_parser.openapi import Endpoint

        result = Endpoint.parse_multipart_body(body)

        assert result is None

    def test_parse_request_json_body(self, mocker):
        schema = mocker.MagicMock()
        body = {"content": {"application/json": {"schema": schema}}}
        property_from_dict = mocker.patch(f"{MODULE_NAME}.property_from_dict")

        from openapi_python_client.openapi_parser.openapi import Endpoint

        result = Endpoint.parse_request_json_body(body)

        property_from_dict.assert_called_once_with("json_body", required=True, data=schema)
        assert result == property_from_dict()

    def test_parse_request_json_body_no_data(self):
        body = {"content": {}}

        from openapi_python_client.openapi_parser.openapi import Endpoint

        result = Endpoint.parse_request_json_body(body)

        assert result is None

    def test_add_body_no_data(self, mocker):
        from openapi_python_client.openapi_parser.openapi import Endpoint

        parse_request_form_body = mocker.patch.object(Endpoint, "parse_request_form_body")
        endpoint = Endpoint(
            path="path",
            method="method",
            description=None,
            name="name",
            requires_security=False,
            tag="tag",
            relative_imports={"import_3"},
        )

        endpoint._add_body({})

        parse_request_form_body.assert_not_called()

    def test_add_body_happy(self, mocker):
        from openapi_python_client.openapi_parser.openapi import Endpoint, Reference
        from openapi_python_client.openapi_parser.properties import Property

        request_body = mocker.MagicMock()
        form_body_reference = Reference.from_ref(ref="a")
        multipart_body_reference = Reference.from_ref(ref="b")
        parse_request_form_body = mocker.patch.object(
            Endpoint, "parse_request_form_body", return_value=form_body_reference
        )
        parse_multipart_body = mocker.patch.object(
            Endpoint, "parse_multipart_body", return_value=multipart_body_reference
        )

        json_body = mocker.MagicMock(autospec=Property)
        json_body_imports = mocker.MagicMock()
        json_body.get_imports.return_value = {json_body_imports}
        parse_request_json_body = mocker.patch.object(Endpoint, "parse_request_json_body", return_value=json_body)
        import_string_from_reference = mocker.patch(
            f"{MODULE_NAME}.import_string_from_reference", side_effect=["import_1", "import_2"]
        )

        endpoint = Endpoint(
            path="path",
            method="method",
            description=None,
            name="name",
            requires_security=False,
            tag="tag",
            relative_imports={"import_3"},
        )

        endpoint._add_body({"requestBody": request_body})

        parse_request_form_body.assert_called_once_with(request_body)
        parse_request_json_body.assert_called_once_with(request_body)
        parse_multipart_body.assert_called_once_with(request_body)
        import_string_from_reference.assert_has_calls(
            [
                mocker.call(form_body_reference, prefix="..models"),
                mocker.call(multipart_body_reference, prefix="..models"),
            ]
        )
        json_body.get_imports.assert_called_once_with(prefix="..models")
        assert endpoint.relative_imports == {"import_1", "import_2", "import_3", json_body_imports}
        assert endpoint.json_body == json_body
        assert endpoint.form_body_reference == form_body_reference
        assert endpoint.multipart_body_reference == multipart_body_reference

    def test__add_responses(self, mocker):
        from openapi_python_client.openapi_parser.openapi import Endpoint, RefResponse, Reference

        response_1_data = mocker.MagicMock()
        response_2_data = mocker.MagicMock()
        data = {"responses": {"200": response_1_data, "404": response_2_data,}}
        endpoint = Endpoint(
            path="path",
            method="method",
            description=None,
            name="name",
            requires_security=False,
            tag="tag",
            relative_imports={"import_3"},
        )
        ref_1 = Reference.from_ref(ref="ref_1")
        ref_2 = Reference.from_ref(ref="ref_2")
        response_1 = RefResponse(status_code=200, reference=ref_1)
        response_2 = RefResponse(status_code=404, reference=ref_2)
        response_from_dict = mocker.patch(f"{MODULE_NAME}.response_from_dict", side_effect=[response_1, response_2])
        import_string_from_reference = mocker.patch(
            f"{MODULE_NAME}.import_string_from_reference", side_effect=["import_1", "import_2"]
        )

        endpoint._add_responses(data)

        response_from_dict.assert_has_calls(
            [mocker.call(status_code=200, data=response_1_data), mocker.call(status_code=404, data=response_2_data),]
        )
        import_string_from_reference.assert_has_calls(
            [mocker.call(ref_1, prefix="..models"), mocker.call(ref_2, prefix="..models"),]
        )
        assert endpoint.responses == [response_1, response_2]
        assert endpoint.relative_imports == {"import_1", "import_2", "import_3"}

    def test__add_parameters_handles_no_params(self):
        from openapi_python_client.openapi_parser.openapi import Endpoint

        endpoint = Endpoint(
            path="path", method="method", description=None, name="name", requires_security=False, tag="tag",
        )
        endpoint._add_parameters({})  # Just checking there's no exception here

    def test__add_parameters_fail_loudly_when_location_not_supported(self, mocker):
        from openapi_python_client.openapi_parser.openapi import Endpoint

        endpoint = Endpoint(
            path="path", method="method", description=None, name="name", requires_security=False, tag="tag",
        )
        mocker.patch(f"{MODULE_NAME}.property_from_dict")

        with pytest.raises(ValueError):
            endpoint._add_parameters(
                {"parameters": [{"name": "test", "required": True, "schema": mocker.MagicMock(), "in": "cookie"}]}
            )

    def test__add_parameters_happy(self, mocker):
        from openapi_python_client.openapi_parser.openapi import Endpoint
        from openapi_python_client.openapi_parser.properties import Property

        endpoint = Endpoint(
            path="path",
            method="method",
            description=None,
            name="name",
            requires_security=False,
            tag="tag",
            relative_imports={"import_3"},
        )
        path_prop = mocker.MagicMock(autospec=Property)
        path_prop_import = mocker.MagicMock()
        path_prop.get_imports = mocker.MagicMock(return_value={path_prop_import})
        query_prop = mocker.MagicMock(autospec=Property)
        query_prop_import = mocker.MagicMock()
        query_prop.get_imports = mocker.MagicMock(return_value={query_prop_import})
        property_from_dict = mocker.patch(f"{MODULE_NAME}.property_from_dict", side_effect=[path_prop, query_prop])
        path_schema = mocker.MagicMock()
        query_schema = mocker.MagicMock()
        data = {
            "parameters": [
                {"name": "path_prop_name", "required": True, "schema": path_schema, "in": "path"},
                {"name": "query_prop_name", "required": False, "schema": query_schema, "in": "query"},
            ]
        }

        endpoint._add_parameters(data)

        property_from_dict.assert_has_calls(
            [
                mocker.call(name="path_prop_name", required=True, data=path_schema),
                mocker.call(name="query_prop_name", required=False, data=query_schema),
            ]
        )
        path_prop.get_imports.assert_called_once_with(prefix="..models")
        query_prop.get_imports.assert_called_once_with(prefix="..models")
        assert endpoint.relative_imports == {
            "import_3",
            path_prop_import,
            query_prop_import,
        }
        assert endpoint.path_parameters == [path_prop]
        assert endpoint.query_parameters == [query_prop]

    def test_from_data(self, mocker):
        from openapi_python_client.openapi_parser.openapi import Endpoint

        path = mocker.MagicMock()
        method = mocker.MagicMock()
        _add_parameters = mocker.patch.object(Endpoint, "_add_parameters")
        _add_responses = mocker.patch.object(Endpoint, "_add_responses")
        _add_body = mocker.patch.object(Endpoint, "_add_body")
        data = {
            "description": mocker.MagicMock(),
            "operationId": mocker.MagicMock(),
            "security": {"blah": "bloo"},
        }

        endpoint = Endpoint.from_data(data=data, path=path, method=method, tag="default")

        assert endpoint.path == path
        assert endpoint.method == method
        assert endpoint.description == data["description"]
        assert endpoint.name == data["operationId"]
        assert endpoint.requires_security
        assert endpoint.tag == "default"
        _add_parameters.assert_called_once_with(data)
        _add_responses.assert_called_once_with(data)
        _add_body.assert_called_once_with(data)

        del data["security"]

        endpoint = Endpoint.from_data(data=data, path=path, method=method, tag="a")

        assert not endpoint.requires_security
        assert endpoint.tag == "a"


class TestImportStringFromReference:
    def test_import_string_from_reference_no_prefix(self, mocker):
        from openapi_python_client.openapi_parser.openapi import import_string_from_reference
        from openapi_python_client.openapi_parser.reference import Reference

        reference = mocker.MagicMock(autospec=Reference)
        result = import_string_from_reference(reference)

        assert result == f"from .{reference.module_name} import {reference.class_name}"

    def test_import_string_from_reference_with_prefix(self, mocker):
        from openapi_python_client.openapi_parser.openapi import import_string_from_reference
        from openapi_python_client.openapi_parser.reference import Reference

        prefix = mocker.MagicMock(autospec=str)
        reference = mocker.MagicMock(autospec=Reference)
        result = import_string_from_reference(reference=reference, prefix=prefix)

        assert result == f"from {prefix}.{reference.module_name} import {reference.class_name}"


class TestEndpointCollection:
    def test_from_dict(self, mocker):
        from openapi_python_client.openapi_parser.openapi import EndpointCollection, Endpoint

        data_1 = {}
        data_2 = {"tags": ["tag_2", "tag_3"]}
        data_3 = {}
        data = {
            "path_1": {"method_1": data_1, "method_2": data_2},
            "path_2": {"method_1": data_3},
        }
        endpoint_1 = mocker.MagicMock(autospec=Endpoint, tag="default", relative_imports={"1", "2"})
        endpoint_2 = mocker.MagicMock(autospec=Endpoint, tag="tag_2", relative_imports={"2"})
        endpoint_3 = mocker.MagicMock(autospec=Endpoint, tag="default", relative_imports={"2", "3"})
        endpoint_from_data = mocker.patch.object(
            Endpoint, "from_data", side_effect=[endpoint_1, endpoint_2, endpoint_3]
        )

        result = EndpointCollection.from_dict(data)

        endpoint_from_data.assert_has_calls(
            [
                mocker.call(data=data_1, path="path_1", method="method_1", tag="default"),
                mocker.call(data=data_2, path="path_1", method="method_2", tag="tag_2"),
                mocker.call(data=data_3, path="path_2", method="method_1", tag="default"),
            ]
        )
        assert result == {
            "default": EndpointCollection(
                "default", endpoints=[endpoint_1, endpoint_3], relative_imports={"1", "2", "3"}
            ),
            "tag_2": EndpointCollection("tag_2", endpoints=[endpoint_2], relative_imports={"2"}),
        }

    def test_from_dict_errors(self, mocker):
        from openapi_python_client.openapi_parser.openapi import EndpointCollection, Endpoint, ParseError

        data_1 = {}
        data_2 = {"tags": ["tag_2", "tag_3"]}
        data_3 = {}
        data = {
            "path_1": {"method_1": data_1, "method_2": data_2},
            "path_2": {"method_1": data_3},
        }
        endpoint_from_data = mocker.patch.object(
            Endpoint, "from_data", side_effect=[ParseError("1"), ParseError("2"), ParseError("3")]
        )

        result = EndpointCollection.from_dict(data)

        endpoint_from_data.assert_has_calls(
            [
                mocker.call(data=data_1, path="path_1", method="method_1", tag="default"),
                mocker.call(data=data_2, path="path_1", method="method_2", tag="tag_2"),
                mocker.call(data=data_3, path="path_2", method="method_1", tag="default"),
            ]
        )
        assert result["default"].parse_errors[0].data == "1"
        assert result["default"].parse_errors[1].data == "3"
        assert result["tag_2"].parse_errors[0].data == "2"
