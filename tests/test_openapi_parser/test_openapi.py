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
            return EnumProperty(name=mocker.MagicMock(), required=True, default=None, values=mocker.MagicMock(),)

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

        enum_1 = EnumProperty(name=mocker.MagicMock(), required=True, default=None, values=mocker.MagicMock(),)
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
        Reference = mocker.patch(f"{MODULE_NAME}.Reference")
        import_string_from_reference = mocker.patch(f"{MODULE_NAME}.import_string_from_reference")

        from openapi_python_client.openapi_parser.openapi import Schema

        result = Schema.from_dict(in_data)

        Reference.assert_called_once_with(in_data["title"])
        property_from_dict.assert_has_calls(
            [
                mocker.call(name="RequiredEnum", required=True, data=in_data["properties"]["RequiredEnum"]),
                mocker.call(name="OptionalString", required=False, data=in_data["properties"]["OptionalString"]),
            ]
        )
        import_string_from_reference.assert_called_once_with(required_property.reference)
        assert result == Schema(
            reference=Reference(),
            required_properties=[required_property],
            optional_properties=[optional_property],
            relative_imports={import_string_from_reference()},
            description=in_data["description"],
        )


class TestEndpoint:
    def test_parse_request_form_body(self, mocker):
        ref = mocker.MagicMock()
        body = {"content": {"application/x-www-form-urlencoded": {"schema": {"$ref": ref}}}}
        Reference = mocker.patch(f"{MODULE_NAME}.Reference")

        from openapi_python_client.openapi_parser.openapi import Endpoint

        result = Endpoint.parse_request_form_body(body)

        Reference.assert_called_once_with(ref)
        assert result == Reference()

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
