import openapi_python_client.schema as oai
from openapi_python_client import GeneratorError
from openapi_python_client.parser.errors import ParseError

MODULE_NAME = "openapi_python_client.parser.openapi"


class TestGeneratorData:
    def test_from_dict(self, mocker):
        build_schemas = mocker.patch(f"{MODULE_NAME}.build_schemas")
        EndpointCollection = mocker.patch(f"{MODULE_NAME}.EndpointCollection")
        schemas = mocker.MagicMock()
        endpoints_collections_by_tag = mocker.MagicMock()
        EndpointCollection.from_data.return_value = (endpoints_collections_by_tag, schemas)
        OpenAPI = mocker.patch(f"{MODULE_NAME}.oai.OpenAPI")
        openapi = OpenAPI.parse_obj.return_value

        in_dict = mocker.MagicMock()

        from openapi_python_client.parser.openapi import GeneratorData

        generator_data = GeneratorData.from_dict(in_dict)

        OpenAPI.parse_obj.assert_called_once_with(in_dict)
        build_schemas.assert_called_once_with(components=openapi.components.schemas)
        EndpointCollection.from_data.assert_called_once_with(data=openapi.paths, schemas=build_schemas.return_value)
        assert generator_data == GeneratorData(
            title=openapi.info.title,
            description=openapi.info.description,
            version=openapi.info.version,
            endpoint_collections_by_tag=endpoints_collections_by_tag,
            errors=schemas.errors,
            models=schemas.models,
            enums=schemas.enums,
        )

        # Test no components
        openapi.components = None
        build_schemas.reset_mock()

        GeneratorData.from_dict(in_dict)

        build_schemas.assert_not_called()

    def test_from_dict_invalid_schema(self, mocker):
        Schemas = mocker.patch(f"{MODULE_NAME}.Schemas")

        in_dict = {}

        from openapi_python_client.parser.openapi import GeneratorData

        generator_data = GeneratorData.from_dict(in_dict)

        assert generator_data == GeneratorError(
            header="Failed to parse OpenAPI document",
            detail=(
                "2 validation errors for OpenAPI\n"
                "info\n"
                "  field required (type=value_error.missing)\n"
                "paths\n"
                "  field required (type=value_error.missing)"
            ),
        )
        Schemas.build.assert_not_called()
        Schemas.assert_not_called()


class TestEndpoint:
    def test_parse_yaml_body(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint, Schemas

        schema = mocker.MagicMock()
        body = oai.RequestBody.construct(content={"text/yaml": oai.MediaType.construct(media_type_schema=schema)})
        property_from_data = mocker.patch(f"{MODULE_NAME}.property_from_data")
        schemas = Schemas()

        result = Endpoint.parse_request_yaml_body(body=body, schemas=schemas, parent_name="parent")

        property_from_data.assert_called_once_with(
            name="yaml_body", required=True, data=schema, schemas=schemas, parent_name="parent"
        )
        assert result == property_from_data.return_value

    def test_parse_yaml_body_no_data(self):
        from openapi_python_client.parser.openapi import Endpoint, Schemas

        body = oai.RequestBody.construct(content={})
        schemas = Schemas()

        result = Endpoint.parse_request_yaml_body(body=body, schemas=schemas, parent_name="parent")

        assert result == (None, schemas)

    def test_parse_request_form_body(self, mocker):
        ref = mocker.MagicMock()
        body = oai.RequestBody.construct(
            content={
                "application/x-www-form-urlencoded": oai.MediaType.construct(
                    media_type_schema=oai.Reference.construct(ref=ref)
                )
            }
        )
        from_ref = mocker.patch(f"{MODULE_NAME}.Reference.from_ref")

        from openapi_python_client.parser.openapi import Endpoint

        result = Endpoint.parse_request_form_body(body)

        from_ref.assert_called_once_with(ref)
        assert result == from_ref()

    def test_parse_request_form_body_no_data(self):
        body = oai.RequestBody.construct(content={})

        from openapi_python_client.parser.openapi import Endpoint

        result = Endpoint.parse_request_form_body(body)

        assert result is None

    def test_parse_multipart_body(self, mocker):
        ref = mocker.MagicMock()
        body = oai.RequestBody.construct(
            content={"multipart/form-data": oai.MediaType.construct(media_type_schema=oai.Reference.construct(ref=ref))}
        )
        from_ref = mocker.patch(f"{MODULE_NAME}.Reference.from_ref")

        from openapi_python_client.parser.openapi import Endpoint

        result = Endpoint.parse_multipart_body(body)

        from_ref.assert_called_once_with(ref)
        assert result == from_ref()

    def test_parse_multipart_body_no_data(self):
        body = oai.RequestBody.construct(content={})

        from openapi_python_client.parser.openapi import Endpoint

        result = Endpoint.parse_multipart_body(body)

        assert result is None

    def test_parse_request_json_body(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint, Schemas

        schema = mocker.MagicMock()
        body = oai.RequestBody.construct(
            content={"application/json": oai.MediaType.construct(media_type_schema=schema)}
        )
        property_from_data = mocker.patch(f"{MODULE_NAME}.property_from_data")
        schemas = Schemas()

        result = Endpoint.parse_request_json_body(body=body, schemas=schemas, parent_name="parent")

        property_from_data.assert_called_once_with(
            name="json_body", required=True, data=schema, schemas=schemas, parent_name="parent"
        )
        assert result == property_from_data.return_value

    def test_parse_request_json_body_no_data(self):
        from openapi_python_client.parser.openapi import Endpoint, Schemas

        body = oai.RequestBody.construct(content={})
        schemas = Schemas()

        result = Endpoint.parse_request_json_body(body=body, schemas=schemas, parent_name="parent")

        assert result == (None, schemas)

    def test_add_body_no_data(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint, Schemas

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
        schemas = Schemas()

        Endpoint._add_body(endpoint=endpoint, data=oai.Operation.construct(), schemas=schemas)

        parse_request_form_body.assert_not_called()

    def test_add_body_bad_data(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint, Schemas

        mocker.patch.object(Endpoint, "parse_request_form_body")
        parse_error = ParseError(data=mocker.MagicMock())
        other_schemas = mocker.MagicMock()
        mocker.patch.object(Endpoint, "parse_request_json_body", return_value=(parse_error, other_schemas))
        endpoint = Endpoint(
            path="path",
            method="method",
            description=None,
            name="name",
            requires_security=False,
            tag="tag",
            relative_imports={"import_3"},
        )
        request_body = mocker.MagicMock()
        schemas = Schemas()

        result = Endpoint._add_body(
            endpoint=endpoint, data=oai.Operation.construct(requestBody=request_body), schemas=schemas
        )

        assert result == (
            ParseError(detail=f"cannot parse body of endpoint {endpoint.name}", data=parse_error.data),
            other_schemas,
        )

    def test_add_body_happy(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint, Reference, Schemas
        from openapi_python_client.parser.properties import Property

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
        parsed_schemas = mocker.MagicMock()
        parse_request_json_body = mocker.patch.object(
            Endpoint, "parse_request_json_body", return_value=(json_body, parsed_schemas)
        )
        yaml_body = mocker.MagicMock(autospec=Property)
        yaml_body_imports = mocker.MagicMock()
        yaml_body.get_imports.return_value = {yaml_body_imports}
        parse_request_yaml_body = mocker.patch.object(
            Endpoint, "parse_request_yaml_body", return_value=(yaml_body, parsed_schemas)
        )
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
        initial_schemas = mocker.MagicMock()

        (endpoint, response_schemas) = Endpoint._add_body(
            endpoint=endpoint, data=oai.Operation.construct(requestBody=request_body), schemas=initial_schemas
        )

        assert response_schemas == parsed_schemas
        parse_request_form_body.assert_called_once_with(request_body)
        parse_request_json_body.assert_called_once_with(body=request_body, schemas=initial_schemas, parent_name="name")
        parse_request_yaml_body.assert_called_once_with(body=request_body, schemas=parsed_schemas, parent_name="name")
        parse_multipart_body.assert_called_once_with(request_body)
        import_string_from_reference.assert_has_calls(
            [
                mocker.call(form_body_reference, prefix="...models"),
                mocker.call(multipart_body_reference, prefix="...models"),
            ]
        )
        yaml_body.get_imports.assert_called_once_with(prefix="...")
        json_body.get_imports.assert_called_once_with(prefix="...")
        assert endpoint.relative_imports == {"import_1", "import_2", "import_3", yaml_body_imports, json_body_imports}
        assert endpoint.yaml_body == yaml_body
        assert endpoint.json_body == json_body
        assert endpoint.form_body_reference == form_body_reference
        assert endpoint.multipart_body_reference == multipart_body_reference

    def test__add_responses_error(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint, Schemas

        schemas = Schemas()
        response_1_data = mocker.MagicMock()
        response_2_data = mocker.MagicMock()
        data = {
            "200": response_1_data,
            "404": response_2_data,
        }
        endpoint = Endpoint(
            path="path",
            method="method",
            description=None,
            name="name",
            requires_security=False,
            tag="tag",
            relative_imports={"import_3"},
        )
        parse_error = ParseError(data=mocker.MagicMock())
        response_from_data = mocker.patch(f"{MODULE_NAME}.response_from_data", return_value=(parse_error, schemas))

        response, schemas = Endpoint._add_responses(endpoint=endpoint, data=data, schemas=schemas)

        response_from_data.assert_has_calls(
            [
                mocker.call(status_code=200, data=response_1_data, schemas=schemas, parent_name="name"),
                mocker.call(status_code=404, data=response_2_data, schemas=schemas, parent_name="name"),
            ]
        )
        assert response.errors == [
            ParseError(
                detail=f"Cannot parse response for status code 200, response will be omitted from generated client",
                data=parse_error.data,
            ),
            ParseError(
                detail=f"Cannot parse response for status code 404, response will be omitted from generated client",
                data=parse_error.data,
            ),
        ]

    def test__add_responses(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint, Response
        from openapi_python_client.parser.properties import DateProperty, DateTimeProperty

        response_1_data = mocker.MagicMock()
        response_2_data = mocker.MagicMock()
        data = {
            "200": response_1_data,
            "404": response_2_data,
        }
        endpoint = Endpoint(
            path="path",
            method="method",
            description=None,
            name="name",
            requires_security=False,
            tag="tag",
            relative_imports={"import_3"},
        )
        schemas = mocker.MagicMock()
        schemas_1 = mocker.MagicMock()
        schemas_2 = mocker.MagicMock()
        response_1 = Response(
            status_code=200,
            source="source",
            prop=DateTimeProperty(name="datetime", required=True, nullable=False, default=None, description=None),
        )
        response_2 = Response(
            status_code=404,
            source="source",
            prop=DateProperty(name="date", required=True, nullable=False, default=None, description=None),
        )
        response_from_data = mocker.patch(
            f"{MODULE_NAME}.response_from_data", side_effect=[(response_1, schemas_1), (response_2, schemas_2)]
        )

        endpoint, response_schemas = Endpoint._add_responses(endpoint=endpoint, data=data, schemas=schemas)

        response_from_data.assert_has_calls(
            [
                mocker.call(status_code=200, data=response_1_data, schemas=schemas, parent_name="name"),
                mocker.call(status_code=404, data=response_2_data, schemas=schemas_1, parent_name="name"),
            ]
        )
        assert endpoint.responses == [response_1, response_2]
        assert endpoint.relative_imports == {
            "from dateutil.parser import isoparse",
            "from typing import cast",
            "import datetime",
            "import_3",
        }
        assert response_schemas == schemas_2

    def test__add_parameters_handles_no_params(self):
        from openapi_python_client.parser.openapi import Endpoint, Schemas

        endpoint = Endpoint(
            path="path",
            method="method",
            description=None,
            name="name",
            requires_security=False,
            tag="tag",
        )
        schemas = Schemas()
        # Just checking there's no exception here
        assert Endpoint._add_parameters(endpoint=endpoint, data=oai.Operation.construct(), schemas=schemas) == (
            endpoint,
            schemas,
        )

    def test__add_parameters_parse_error(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint

        endpoint = Endpoint(
            path="path",
            method="method",
            description=None,
            name="name",
            requires_security=False,
            tag="tag",
        )
        initial_schemas = mocker.MagicMock()
        parse_error = ParseError(data=mocker.MagicMock())
        property_schemas = mocker.MagicMock()
        mocker.patch(f"{MODULE_NAME}.property_from_data", return_value=(parse_error, property_schemas))
        param = oai.Parameter.construct(name="test", required=True, param_schema=mocker.MagicMock(), param_in="cookie")

        result = Endpoint._add_parameters(
            endpoint=endpoint, data=oai.Operation.construct(parameters=[param]), schemas=initial_schemas
        )
        assert result == (
            ParseError(data=parse_error.data, detail=f"cannot parse parameter of endpoint {endpoint.name}"),
            property_schemas,
        )

    def test__add_parameters_fail_loudly_when_location_not_supported(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint, Schemas

        endpoint = Endpoint(
            path="path",
            method="method",
            description=None,
            name="name",
            requires_security=False,
            tag="tag",
        )
        parsed_schemas = mocker.MagicMock()
        mocker.patch(f"{MODULE_NAME}.property_from_data", return_value=(mocker.MagicMock(), parsed_schemas))
        param = oai.Parameter.construct(name="test", required=True, param_schema=mocker.MagicMock(), param_in="cookie")
        schemas = Schemas()

        result = Endpoint._add_parameters(
            endpoint=endpoint, data=oai.Operation.construct(parameters=[param]), schemas=schemas
        )
        assert result == (ParseError(data=param, detail="Parameter must be declared in path or query"), parsed_schemas)

    def test__add_parameters_happy(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint
        from openapi_python_client.parser.properties import Property

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
        header_prop = mocker.MagicMock(autospec=Property)
        header_prop_import = mocker.MagicMock()
        header_prop.get_imports = mocker.MagicMock(return_value={header_prop_import})
        schemas_1 = mocker.MagicMock()
        schemas_2 = mocker.MagicMock()
        schemas_3 = mocker.MagicMock()
        property_from_data = mocker.patch(
            f"{MODULE_NAME}.property_from_data",
            side_effect=[(path_prop, schemas_1), (query_prop, schemas_2), (header_prop, schemas_3)],
        )
        path_schema = mocker.MagicMock()
        query_schema = mocker.MagicMock()
        header_schema = mocker.MagicMock()
        data = oai.Operation.construct(
            parameters=[
                oai.Parameter.construct(
                    name="path_prop_name", required=True, param_schema=path_schema, param_in="path"
                ),
                oai.Parameter.construct(
                    name="query_prop_name", required=False, param_schema=query_schema, param_in="query"
                ),
                oai.Parameter.construct(
                    name="header_prop_name", required=False, param_schema=header_schema, param_in="header"
                ),
                oai.Reference.construct(),  # Should be ignored
                oai.Parameter.construct(),  # Should be ignored
            ]
        )
        initial_schemas = mocker.MagicMock()

        (endpoint, schemas) = Endpoint._add_parameters(endpoint=endpoint, data=data, schemas=initial_schemas)

        property_from_data.assert_has_calls(
            [
                mocker.call(
                    name="path_prop_name", required=True, data=path_schema, schemas=initial_schemas, parent_name="name"
                ),
                mocker.call(
                    name="query_prop_name", required=False, data=query_schema, schemas=schemas_1, parent_name="name"
                ),
                mocker.call(
                    name="header_prop_name", required=False, data=header_schema, schemas=schemas_2, parent_name="name"
                ),
            ]
        )
        path_prop.get_imports.assert_called_once_with(prefix="...")
        query_prop.get_imports.assert_called_once_with(prefix="...")
        header_prop.get_imports.assert_called_once_with(prefix="...")
        assert endpoint.relative_imports == {"import_3", path_prop_import, query_prop_import, header_prop_import}
        assert endpoint.path_parameters == [path_prop]
        assert endpoint.query_parameters == [query_prop]
        assert endpoint.header_parameters == [header_prop]
        assert schemas == schemas_3

    def test_from_data_bad_params(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint

        path = mocker.MagicMock()
        method = mocker.MagicMock()
        parse_error = ParseError(data=mocker.MagicMock())
        return_schemas = mocker.MagicMock()
        _add_parameters = mocker.patch.object(Endpoint, "_add_parameters", return_value=(parse_error, return_schemas))
        data = oai.Operation.construct(
            description=mocker.MagicMock(),
            operationId=mocker.MagicMock(),
            security={"blah": "bloo"},
            responses=mocker.MagicMock(),
        )
        inital_schemas = mocker.MagicMock()

        result = Endpoint.from_data(data=data, path=path, method=method, tag="default", schemas=inital_schemas)

        assert result == (parse_error, return_schemas)

    def test_from_data_bad_responses(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint

        path = mocker.MagicMock()
        method = mocker.MagicMock()
        parse_error = ParseError(data=mocker.MagicMock())
        param_schemas = mocker.MagicMock()
        _add_parameters = mocker.patch.object(
            Endpoint, "_add_parameters", return_value=(mocker.MagicMock(), param_schemas)
        )
        response_schemas = mocker.MagicMock()
        _add_responses = mocker.patch.object(Endpoint, "_add_responses", return_value=(parse_error, response_schemas))
        data = oai.Operation.construct(
            description=mocker.MagicMock(),
            operationId=mocker.MagicMock(),
            security={"blah": "bloo"},
            responses=mocker.MagicMock(),
        )
        initial_schemas = mocker.MagicMock()

        result = Endpoint.from_data(data=data, path=path, method=method, tag="default", schemas=initial_schemas)

        assert result == (parse_error, response_schemas)

    def test_from_data_standard(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint

        path = mocker.MagicMock()
        method = mocker.MagicMock()
        param_schemas = mocker.MagicMock()
        param_endpoint = mocker.MagicMock()
        _add_parameters = mocker.patch.object(Endpoint, "_add_parameters", return_value=(param_endpoint, param_schemas))
        response_schemas = mocker.MagicMock()
        response_endpoint = mocker.MagicMock()
        _add_responses = mocker.patch.object(
            Endpoint, "_add_responses", return_value=(response_endpoint, response_schemas)
        )
        body_schemas = mocker.MagicMock()
        body_endpoint = mocker.MagicMock()
        _add_body = mocker.patch.object(Endpoint, "_add_body", return_value=(body_endpoint, body_schemas))
        data = oai.Operation.construct(
            description=mocker.MagicMock(),
            operationId=mocker.MagicMock(),
            security={"blah": "bloo"},
            responses=mocker.MagicMock(),
        )
        initial_schemas = mocker.MagicMock()

        mocker.patch("openapi_python_client.utils.remove_string_escapes", return_value=data.description)

        endpoint = Endpoint.from_data(data=data, path=path, method=method, tag="default", schemas=initial_schemas)

        assert endpoint == _add_body.return_value

        _add_parameters.assert_called_once_with(
            endpoint=Endpoint(
                path=path,
                method=method,
                description=data.description,
                name=data.operationId,
                requires_security=True,
                tag="default",
            ),
            data=data,
            schemas=initial_schemas,
        )
        _add_responses.assert_called_once_with(endpoint=param_endpoint, data=data.responses, schemas=param_schemas)
        _add_body.assert_called_once_with(endpoint=response_endpoint, data=data, schemas=response_schemas)

    def test_from_data_no_operation_id(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint

        path = "/path/with/{param}/"
        method = "get"
        _add_parameters = mocker.patch.object(
            Endpoint, "_add_parameters", return_value=(mocker.MagicMock(), mocker.MagicMock())
        )
        _add_responses = mocker.patch.object(
            Endpoint, "_add_responses", return_value=(mocker.MagicMock(), mocker.MagicMock())
        )
        _add_body = mocker.patch.object(Endpoint, "_add_body", return_value=(mocker.MagicMock(), mocker.MagicMock()))
        data = oai.Operation.construct(
            description=mocker.MagicMock(),
            operationId=None,
            security={"blah": "bloo"},
            responses=mocker.MagicMock(),
        )
        schemas = mocker.MagicMock()
        mocker.patch("openapi_python_client.utils.remove_string_escapes", return_value=data.description)

        result = Endpoint.from_data(data=data, path=path, method=method, tag="default", schemas=schemas)

        assert result == _add_body.return_value

        _add_parameters.assert_called_once_with(
            endpoint=Endpoint(
                path=path,
                method=method,
                description=data.description,
                name="get_path_with_param",
                requires_security=True,
                tag="default",
            ),
            data=data,
            schemas=schemas,
        )
        _add_responses.assert_called_once_with(
            endpoint=_add_parameters.return_value[0], data=data.responses, schemas=_add_parameters.return_value[1]
        )
        _add_body.assert_called_once_with(
            endpoint=_add_responses.return_value[0], data=data, schemas=_add_responses.return_value[1]
        )

    def test_from_data_no_security(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint

        data = oai.Operation.construct(
            description=mocker.MagicMock(),
            operationId=mocker.MagicMock(),
            security=None,
            responses=mocker.MagicMock(),
        )
        _add_parameters = mocker.patch.object(
            Endpoint, "_add_parameters", return_value=(mocker.MagicMock(), mocker.MagicMock())
        )
        _add_responses = mocker.patch.object(
            Endpoint, "_add_responses", return_value=(mocker.MagicMock(), mocker.MagicMock())
        )
        _add_body = mocker.patch.object(Endpoint, "_add_body", return_value=(mocker.MagicMock(), mocker.MagicMock()))
        path = mocker.MagicMock()
        method = mocker.MagicMock()
        mocker.patch("openapi_python_client.utils.remove_string_escapes", return_value=data.description)
        schemas = mocker.MagicMock()

        Endpoint.from_data(data=data, path=path, method=method, tag="a", schemas=schemas)

        _add_parameters.assert_called_once_with(
            endpoint=Endpoint(
                path=path,
                method=method,
                description=data.description,
                name=data.operationId,
                requires_security=False,
                tag="a",
            ),
            data=data,
            schemas=schemas,
        )
        _add_responses.assert_called_once_with(
            endpoint=_add_parameters.return_value[0], data=data.responses, schemas=_add_parameters.return_value[1]
        )
        _add_body.assert_called_once_with(
            endpoint=_add_responses.return_value[0], data=data, schemas=_add_responses.return_value[1]
        )


class TestImportStringFromReference:
    def test_import_string_from_reference_no_prefix(self, mocker):
        from openapi_python_client.parser.openapi import import_string_from_reference
        from openapi_python_client.parser.reference import Reference

        reference = mocker.MagicMock(autospec=Reference)
        result = import_string_from_reference(reference)

        assert result == f"from .{reference.module_name} import {reference.class_name}"

    def test_import_string_from_reference_with_prefix(self, mocker):
        from openapi_python_client.parser.openapi import import_string_from_reference
        from openapi_python_client.parser.reference import Reference

        prefix = mocker.MagicMock(autospec=str)
        reference = mocker.MagicMock(autospec=Reference)
        result = import_string_from_reference(reference=reference, prefix=prefix)

        assert result == f"from {prefix}.{reference.module_name} import {reference.class_name}"


class TestEndpointCollection:
    def test_from_data(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint, EndpointCollection

        path_1_put = oai.Operation.construct()
        path_1_post = oai.Operation.construct(tags=["tag_2", "tag_3"])
        path_2_get = oai.Operation.construct()
        data = {
            "path_1": oai.PathItem.construct(post=path_1_post, put=path_1_put),
            "path_2": oai.PathItem.construct(get=path_2_get),
        }
        endpoint_1 = mocker.MagicMock(autospec=Endpoint, tag="default", relative_imports={"1", "2"})
        endpoint_2 = mocker.MagicMock(autospec=Endpoint, tag="tag_2", relative_imports={"2"})
        endpoint_3 = mocker.MagicMock(autospec=Endpoint, tag="default", relative_imports={"2", "3"})
        schemas_1 = mocker.MagicMock()
        schemas_2 = mocker.MagicMock()
        schemas_3 = mocker.MagicMock()
        endpoint_from_data = mocker.patch.object(
            Endpoint,
            "from_data",
            side_effect=[(endpoint_1, schemas_1), (endpoint_2, schemas_2), (endpoint_3, schemas_3)],
        )
        schemas = mocker.MagicMock()

        result = EndpointCollection.from_data(data=data, schemas=schemas)

        endpoint_from_data.assert_has_calls(
            [
                mocker.call(data=path_1_put, path="path_1", method="put", tag="default", schemas=schemas),
                mocker.call(data=path_1_post, path="path_1", method="post", tag="tag_2", schemas=schemas_1),
                mocker.call(data=path_2_get, path="path_2", method="get", tag="default", schemas=schemas_2),
            ],
        )
        assert result == (
            {
                "default": EndpointCollection("default", endpoints=[endpoint_1, endpoint_3]),
                "tag_2": EndpointCollection("tag_2", endpoints=[endpoint_2]),
            },
            schemas_3,
        )

    def test_from_data_errors(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint, EndpointCollection, ParseError

        path_1_put = oai.Operation.construct()
        path_1_post = oai.Operation.construct(tags=["tag_2", "tag_3"])
        path_2_get = oai.Operation.construct()
        data = {
            "path_1": oai.PathItem.construct(post=path_1_post, put=path_1_put),
            "path_2": oai.PathItem.construct(get=path_2_get),
        }
        schemas_1 = mocker.MagicMock()
        schemas_2 = mocker.MagicMock()
        schemas_3 = mocker.MagicMock()
        endpoint_from_data = mocker.patch.object(
            Endpoint,
            "from_data",
            side_effect=[
                (ParseError(data="1"), schemas_1),
                (ParseError(data="2"), schemas_2),
                (mocker.MagicMock(errors=[ParseError(data="3")]), schemas_3),
            ],
        )
        schemas = mocker.MagicMock()

        result, result_schemas = EndpointCollection.from_data(data=data, schemas=schemas)

        endpoint_from_data.assert_has_calls(
            [
                mocker.call(data=path_1_put, path="path_1", method="put", tag="default", schemas=schemas),
                mocker.call(data=path_1_post, path="path_1", method="post", tag="tag_2", schemas=schemas_1),
                mocker.call(data=path_2_get, path="path_2", method="get", tag="default", schemas=schemas_2),
            ],
        )
        assert result["default"].parse_errors[0].data == "1"
        assert result["default"].parse_errors[1].data == "3"
        assert result["tag_2"].parse_errors[0].data == "2"
        assert result_schemas == schemas_3
