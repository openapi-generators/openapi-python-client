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
        enums = mocker.MagicMock()
        _check_enums = mocker.patch(f"{MODULE_NAME}.OpenAPI._check_enums", return_value=enums)

        from openapi_python_client.openapi_parser.openapi import OpenAPI

        openapi = OpenAPI.from_dict(in_dict)

        Schema.dict.assert_called_once_with(in_dict["components"]["schemas"])
        EndpointCollection.from_dict.assert_called_once_with(in_dict["paths"])
        _check_enums.assert_called_once_with(schemas.values(), endpoint_collections_by_tag.values())
        assert openapi == OpenAPI(
            title=in_dict["info"]["title"],
            description=in_dict["info"]["description"],
            version=in_dict["info"]["version"],
            endpoint_collections_by_tag=endpoint_collections_by_tag,
            schemas=schemas,
            enums=enums,
        )

    def test__check_enums(self, mocker):
        # Test that all required and optional properties of all schemas are checked
        # Test that all path and query params of all endpoints of all collections are checked
        # Test that non EnumProperties are skipped
        from openapi_python_client.openapi_parser.openapi import EndpointCollection, OpenAPI
        from openapi_python_client.openapi_parser.properties import EnumProperty, StringProperty

        def _make_enum():
            return EnumProperty(name=str(mocker.MagicMock()), required=True, default=None, values=mocker.MagicMock(),)

        # Multiple schemas with both required and optional properties for making sure iteration works correctly
        schema_1 = mocker.MagicMock()
        schema_1_req_enum_1 = _make_enum()
        schema_1_req_enum_2 = _make_enum()
        schema_1.required_properties = [schema_1_req_enum_1, schema_1_req_enum_2]
        schema_1_opt_enum_1 = _make_enum()
        schema_1_opt_enum_2 = _make_enum()
        non_enum = mocker.MagicMock(autospec=StringProperty)  # For checking non-enum properties
        schema_1.optional_properties = [schema_1_opt_enum_1, schema_1_opt_enum_2, non_enum]
        schema_2 = mocker.MagicMock()
        schema_2_req_enum = _make_enum()
        schema_2.required_properties = [schema_2_req_enum]
        schema_2_opt_enum = _make_enum()
        schema_2.optional_properties = [schema_2_opt_enum]
        schemas = [schema_1, schema_2]

        collection_1 = mocker.MagicMock(autospec=EndpointCollection)
        collection_1_endpoint_1 = mocker.MagicMock()
        collection_1_endpoint_1_path_enum_1 = _make_enum()
        collection_1_endpoint_1_path_enum_2 = _make_enum()
        collection_1_endpoint_1.path_parameters = [
            collection_1_endpoint_1_path_enum_1,
            collection_1_endpoint_1_path_enum_2,
        ]
        collection_1_endpoint_1_query_enum_1 = _make_enum()
        collection_1_endpoint_1_query_enum_2 = _make_enum()
        collection_1_endpoint_1.query_parameters = [
            collection_1_endpoint_1_query_enum_1,
            collection_1_endpoint_1_query_enum_2,
        ]
        collection_1_endpoint_2 = mocker.MagicMock()
        collection_1_endpoint_2_path_enum = _make_enum()
        collection_1_endpoint_2.path_parameters = [collection_1_endpoint_2_path_enum]
        collection_1_endpoint_2_query_enum = _make_enum()
        collection_1_endpoint_2.query_parameters = [collection_1_endpoint_2_query_enum]
        collection_1.endpoints = [collection_1_endpoint_1, collection_1_endpoint_2]

        collection_2 = mocker.MagicMock()
        collection_2_endpoint = mocker.MagicMock()
        collection_2_path_enum = _make_enum()
        collection_2_endpoint.path_parameters = [collection_2_path_enum]
        collection_2_query_enum = _make_enum()
        collection_2_endpoint.query_parameters = [collection_2_query_enum]
        collection_2.endpoints = [collection_2_endpoint]
        collections = [collection_1, collection_2]

        enums = {
            schema_1_req_enum_1.reference.class_name: schema_1_req_enum_1,
            schema_1_req_enum_2.reference.class_name: schema_1_req_enum_2,
            schema_1_opt_enum_1.reference.class_name: schema_1_opt_enum_1,
            schema_1_opt_enum_2.reference.class_name: schema_1_opt_enum_2,
            schema_2_req_enum.reference.class_name: schema_2_req_enum,
            schema_2_opt_enum.reference.class_name: schema_2_opt_enum,
            collection_1_endpoint_1_path_enum_1.reference.class_name: collection_1_endpoint_1_path_enum_1,
            collection_1_endpoint_1_path_enum_2.reference.class_name: collection_1_endpoint_1_path_enum_2,
            collection_1_endpoint_1_query_enum_1.reference.class_name: collection_1_endpoint_1_query_enum_1,
            collection_1_endpoint_1_query_enum_2.reference.class_name: collection_1_endpoint_1_query_enum_2,
            collection_1_endpoint_2_path_enum.reference.class_name: collection_1_endpoint_2_path_enum,
            collection_1_endpoint_2_query_enum.reference.class_name: collection_1_endpoint_2_query_enum,
            collection_2_path_enum.reference.class_name: collection_2_path_enum,
            collection_2_query_enum.reference.class_name: collection_2_query_enum,
        }

        result = OpenAPI._check_enums(schemas=schemas, collections=collections)

        assert result == enums

    def test__check_enums_bad_duplicate(self, mocker):
        from dataclasses import replace
        from openapi_python_client.openapi_parser.properties import EnumProperty
        from openapi_python_client.openapi_parser.openapi import OpenAPI

        schema = mocker.MagicMock()

        enum_1 = EnumProperty(name=str(mocker.MagicMock()), required=True, default=None, values=mocker.MagicMock(),)
        enum_2 = replace(enum_1, values=mocker.MagicMock())
        schema.required_properties = [enum_1, enum_2]

        with pytest.raises(AssertionError):
            OpenAPI._check_enums([schema], [])


class TestSchema:
    def test_dict(self, mocker):
        from_dict = mocker.patch(f"{MODULE_NAME}.Schema.from_dict")
        in_data = {1: mocker.MagicMock(), 2: mocker.MagicMock()}
        schema_1 = mocker.MagicMock()
        schema_2 = mocker.MagicMock()
        from_dict.side_effect = [schema_1, schema_2]

        from openapi_python_client.openapi_parser.openapi import Schema

        result = Schema.dict(in_data)

        from_dict.assert_has_calls([mocker.call(value) for value in in_data.values()])
        assert result == {
            schema_1.reference.class_name: schema_1,
            schema_2.reference.class_name: schema_2,
        }

    def test_from_dict(self, mocker):
        from openapi_python_client.openapi_parser.properties import EnumProperty, StringProperty

        in_data = {
            "title": mocker.MagicMock(),
            "description": mocker.MagicMock(),
            "required": ["RequiredEnum"],
            "properties": {"RequiredEnum": mocker.MagicMock(), "OptionalString": mocker.MagicMock(),},
        }
        required_property = EnumProperty(name="RequiredEnum", required=True, default=None, values={},)
        optional_property = StringProperty(name="OptionalString", required=False, default=None)
        property_from_dict = mocker.patch(
            f"{MODULE_NAME}.property_from_dict", side_effect=[required_property, optional_property]
        )
        from_ref = mocker.patch(f"{MODULE_NAME}.Reference.from_ref")
        import_string_from_reference = mocker.patch(f"{MODULE_NAME}.import_string_from_reference")

        from openapi_python_client.openapi_parser.openapi import Schema

        result = Schema.from_dict(in_data)

        from_ref.assert_called_once_with(in_data["title"])
        property_from_dict.assert_has_calls(
            [
                mocker.call(name="RequiredEnum", required=True, data=in_data["properties"]["RequiredEnum"]),
                mocker.call(name="OptionalString", required=False, data=in_data["properties"]["OptionalString"]),
            ]
        )
        import_string_from_reference.assert_called_once_with(required_property.reference)
        assert result == Schema(
            reference=from_ref(),
            required_properties=[required_property],
            optional_properties=[optional_property],
            relative_imports={import_string_from_reference()},
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
        from openapi_python_client.openapi_parser.openapi import Endpoint, Reference, RefProperty

        request_body = mocker.MagicMock()
        form_body_reference = Reference.from_ref(ref="a")
        parse_request_form_body = mocker.patch.object(
            Endpoint, "parse_request_form_body", return_value=form_body_reference
        )
        json_body = RefProperty(name="name", required=True, default=None, reference=Reference.from_ref("b"))
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
        import_string_from_reference.assert_has_calls(
            [mocker.call(form_body_reference, prefix="..models"), mocker.call(json_body.reference, prefix="..models")]
        )
        assert endpoint.relative_imports == {"import_1", "import_2", "import_3"}
        assert endpoint.json_body == json_body
        assert endpoint.form_body_reference == form_body_reference

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
        from openapi_python_client.openapi_parser.openapi import Endpoint, EnumProperty

        endpoint = Endpoint(
            path="path",
            method="method",
            description=None,
            name="name",
            requires_security=False,
            tag="tag",
            relative_imports={"import_3"},
        )
        path_prop = EnumProperty(name="path_enum", required=True, default=None, values={})
        query_prop = EnumProperty(name="query_enum", required=False, default=None, values={})
        propety_from_dict = mocker.patch(f"{MODULE_NAME}.property_from_dict", side_effect=[path_prop, query_prop])
        path_schema = mocker.MagicMock()
        query_schema = mocker.MagicMock()
        import_string_from_reference = mocker.patch(
            f"{MODULE_NAME}.import_string_from_reference", side_effect=["import_1", "import_2"]
        )
        data = {
            "parameters": [
                {"name": "path_prop_name", "required": True, "schema": path_schema, "in": "path"},
                {"name": "query_prop_name", "required": False, "schema": query_schema, "in": "query"},
            ]
        }

        endpoint._add_parameters(data)

        propety_from_dict.assert_has_calls(
            [
                mocker.call(name="path_prop_name", required=True, data=path_schema),
                mocker.call(name="query_prop_name", required=False, data=query_schema),
            ]
        )
        import_string_from_reference.assert_has_calls(
            [mocker.call(path_prop.reference, prefix="..models"), mocker.call(query_prop.reference, prefix="..models"),]
        )
        assert endpoint.relative_imports == {"import_1", "import_2", "import_3"}
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

        endpoint = Endpoint.from_data(data=data, path=path, method=method)

        assert endpoint.path == path
        assert endpoint.method == method
        assert endpoint.description == data["description"]
        assert endpoint.name == data["operationId"]
        assert endpoint.requires_security
        assert endpoint.tag == "default"
        _add_parameters.assert_called_once_with(data)
        _add_responses.assert_called_once_with(data)
        _add_body.assert_called_once_with(data)

        data["tags"] = ["a", "b"]
        del data["security"]

        endpoint = Endpoint.from_data(data=data, path=path, method=method)

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

        data_1 = mocker.MagicMock()
        data_2 = mocker.MagicMock()
        data_3 = mocker.MagicMock()
        data = {
            "path_1": {"method_1": data_1, "method_2": data_2,},
            "path_2": {"method_1": data_3,},
        }
        endpoint_1 = mocker.MagicMock(autospec=Endpoint, tag="tag_1", relative_imports={"1", "2"})
        endpoint_2 = mocker.MagicMock(autospec=Endpoint, tag="tag_2", relative_imports={"2"})
        endpoint_3 = mocker.MagicMock(autospec=Endpoint, tag="tag_1", relative_imports={"2", "3"})
        endpoint_from_data = mocker.patch.object(
            Endpoint, "from_data", side_effect=[endpoint_1, endpoint_2, endpoint_3]
        )

        result = EndpointCollection.from_dict(data)

        endpoint_from_data.assert_has_calls(
            [
                mocker.call(data=data_1, path="path_1", method="method_1"),
                mocker.call(data=data_2, path="path_1", method="method_2"),
                mocker.call(data=data_3, path="path_2", method="method_1"),
            ]
        )
        assert result == {
            "tag_1": EndpointCollection("tag_1", endpoints=[endpoint_1, endpoint_3], relative_imports={"1", "2", "3"}),
            "tag_2": EndpointCollection("tag_2", endpoints=[endpoint_2], relative_imports={"2"}),
        }
