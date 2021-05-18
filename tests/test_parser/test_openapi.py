from unittest.mock import MagicMock

import pytest

import openapi_python_client.schema as oai
from openapi_python_client import GeneratorError
from openapi_python_client.parser.errors import ParseError

MODULE_NAME = "openapi_python_client.parser.openapi"


class TestGeneratorData:
    def test_from_dict(self, mocker, model_property_factory, enum_property_factory):
        from openapi_python_client.parser.properties import Schemas

        build_schemas = mocker.patch(f"{MODULE_NAME}.build_schemas")
        EndpointCollection = mocker.patch(f"{MODULE_NAME}.EndpointCollection")
        schemas = mocker.MagicMock()
        schemas.classes_by_name = {
            "Model": model_property_factory(),
            "Enum": enum_property_factory(),
        }
        endpoints_collections_by_tag = mocker.MagicMock()
        EndpointCollection.from_data.return_value = (endpoints_collections_by_tag, schemas)
        OpenAPI = mocker.patch(f"{MODULE_NAME}.oai.OpenAPI")
        openapi = OpenAPI.parse_obj.return_value
        openapi.openapi = mocker.MagicMock(major=3)
        config = mocker.MagicMock()
        in_dict = mocker.MagicMock()

        from openapi_python_client.parser.openapi import GeneratorData

        generator_data = GeneratorData.from_dict(in_dict, config=config)

        OpenAPI.parse_obj.assert_called_once_with(in_dict)
        build_schemas.assert_called_once_with(components=openapi.components.schemas, config=config, schemas=Schemas())
        EndpointCollection.from_data.assert_called_once_with(
            data=openapi.paths, schemas=build_schemas.return_value, config=config
        )
        assert generator_data.title == openapi.info.title
        assert generator_data.description == openapi.info.description
        assert generator_data.version == openapi.info.version
        assert generator_data.endpoint_collections_by_tag == endpoints_collections_by_tag
        assert generator_data.errors == schemas.errors
        assert list(generator_data.models) == [schemas.classes_by_name["Model"]]
        assert list(generator_data.enums) == [schemas.classes_by_name["Enum"]]

        # Test no components
        openapi.components = None
        build_schemas.reset_mock()

        GeneratorData.from_dict(in_dict, config=config)

        build_schemas.assert_not_called()

    def test_from_dict_invalid_schema(self, mocker):
        Schemas = mocker.patch(f"{MODULE_NAME}.Schemas")
        config = mocker.MagicMock()

        in_dict = {}

        from openapi_python_client.parser.openapi import GeneratorData

        generator_data = GeneratorData.from_dict(in_dict, config=config)

        assert generator_data == GeneratorError(
            header="Failed to parse OpenAPI document",
            detail=(
                "3 validation errors for OpenAPI\n"
                "info\n"
                "  field required (type=value_error.missing)\n"
                "paths\n"
                "  field required (type=value_error.missing)\n"
                "openapi\n"
                "  field required (type=value_error.missing)"
            ),
        )
        Schemas.build.assert_not_called()
        Schemas.assert_not_called()

    def test_swagger_document_invalid_schema(self, mocker):
        Schemas = mocker.patch(f"{MODULE_NAME}.Schemas")
        config = mocker.MagicMock()

        in_dict = {"swagger": "2.0"}

        from openapi_python_client.parser.openapi import GeneratorData

        generator_data = GeneratorData.from_dict(in_dict, config=config)

        assert generator_data == GeneratorError(
            header="Failed to parse OpenAPI document",
            detail=(
                "You may be trying to use a Swagger document; this is not supported by this project.\n\n"
                "3 validation errors for OpenAPI\n"
                "info\n"
                "  field required (type=value_error.missing)\n"
                "paths\n"
                "  field required (type=value_error.missing)\n"
                "openapi\n"
                "  field required (type=value_error.missing)"
            ),
        )
        Schemas.build.assert_not_called()
        Schemas.assert_not_called()

    def test_from_dict_invalid_version(self, mocker):
        Schemas = mocker.patch(f"{MODULE_NAME}.Schemas")
        OpenAPI = mocker.patch(f"{MODULE_NAME}.oai.OpenAPI")
        openapi = OpenAPI.parse_obj.return_value
        openapi.openapi = oai.SemVer("2.1.3")
        in_dict = mocker.MagicMock()
        config = mocker.MagicMock()

        from openapi_python_client.parser.openapi import GeneratorData

        generator_data = GeneratorData.from_dict(in_dict, config=config)

        assert generator_data == GeneratorError(
            header="openapi-python-client only supports OpenAPI 3.x",
            detail="The version of the provided document was 2.1.3",
        )
        Schemas.build.assert_not_called()
        Schemas.assert_not_called()


class TestEndpoint:
    def make_endpoint(self):
        from openapi_python_client.parser.openapi import Endpoint

        return Endpoint(
            path="path",
            method="method",
            description=None,
            name="name",
            requires_security=False,
            tag="tag",
            relative_imports={"import_3"},
        )

    def test_parse_request_form_body(self, mocker):
        ref = mocker.MagicMock()
        body = oai.RequestBody.construct(
            content={
                "application/x-www-form-urlencoded": oai.MediaType.construct(
                    media_type_schema=oai.Reference.construct(ref=ref)
                )
            }
        )
        from_string = mocker.patch(f"{MODULE_NAME}.Class.from_string")
        config = mocker.MagicMock()

        from openapi_python_client.parser.openapi import Endpoint

        result = Endpoint.parse_request_form_body(body=body, config=config)

        from_string.assert_called_once_with(string=ref, config=config)
        assert result == from_string.return_value

    def test_parse_request_form_body_no_data(self):
        body = oai.RequestBody.construct(content={})
        config = MagicMock()

        from openapi_python_client.parser.openapi import Endpoint

        result = Endpoint.parse_request_form_body(body=body, config=config)

        assert result is None

    def test_parse_multipart_body(self, mocker):
        ref = mocker.MagicMock()
        body = oai.RequestBody.construct(
            content={"multipart/form-data": oai.MediaType.construct(media_type_schema=oai.Reference.construct(ref=ref))}
        )
        from_string = mocker.patch(f"{MODULE_NAME}.Class.from_string")
        config = MagicMock()

        from openapi_python_client.parser.openapi import Endpoint

        result = Endpoint.parse_multipart_body(body=body, config=config)

        from_string.assert_called_once_with(string=ref, config=config)
        assert result == from_string.return_value

    def test_parse_multipart_body_no_data(self):
        body = oai.RequestBody.construct(content={})

        from openapi_python_client.parser.openapi import Endpoint

        result = Endpoint.parse_multipart_body(body=body, config=MagicMock())

        assert result is None

    def test_parse_request_json_body(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint, Schemas

        schema = mocker.MagicMock()
        body = oai.RequestBody.construct(
            content={"application/json": oai.MediaType.construct(media_type_schema=schema)}
        )
        property_from_data = mocker.patch(f"{MODULE_NAME}.property_from_data")
        schemas = Schemas()
        config = MagicMock()

        result = Endpoint.parse_request_json_body(body=body, schemas=schemas, parent_name="parent", config=config)

        property_from_data.assert_called_once_with(
            name="json_body", required=True, data=schema, schemas=schemas, parent_name="parent", config=config
        )
        assert result == property_from_data.return_value

    def test_parse_request_json_body_no_data(self):
        from openapi_python_client.parser.openapi import Endpoint, Schemas

        body = oai.RequestBody.construct(content={})
        schemas = Schemas()

        result = Endpoint.parse_request_json_body(body=body, schemas=schemas, parent_name="parent", config=MagicMock())

        assert result == (None, schemas)

    def test_add_body_no_data(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint, Schemas

        parse_request_form_body = mocker.patch.object(Endpoint, "parse_request_form_body")
        endpoint = self.make_endpoint()
        schemas = Schemas()

        Endpoint._add_body(endpoint=endpoint, data=oai.Operation.construct(), schemas=schemas, config=MagicMock())

        parse_request_form_body.assert_not_called()

    def test_add_body_bad_data(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint, Schemas

        mocker.patch.object(Endpoint, "parse_request_form_body")
        parse_error = ParseError(data=mocker.MagicMock(), detail=mocker.MagicMock())
        other_schemas = mocker.MagicMock()
        mocker.patch.object(Endpoint, "parse_request_json_body", return_value=(parse_error, other_schemas))
        endpoint = self.make_endpoint()
        request_body = mocker.MagicMock()
        schemas = Schemas()

        result = Endpoint._add_body(
            endpoint=endpoint,
            data=oai.Operation.construct(requestBody=request_body),
            schemas=schemas,
            config=MagicMock(),
        )

        assert result == (
            ParseError(
                header=f"Cannot parse body of endpoint {endpoint.name}",
                detail=parse_error.detail,
                data=parse_error.data,
            ),
            other_schemas,
        )

    def test_add_body_happy(self, mocker):
        from openapi_python_client.parser.openapi import Class, Endpoint
        from openapi_python_client.parser.properties import Property

        request_body = mocker.MagicMock()
        config = mocker.MagicMock()
        form_body_class = Class(name="A", module_name="a")
        multipart_body_class = Class(name="B", module_name="b")
        parse_request_form_body = mocker.patch.object(Endpoint, "parse_request_form_body", return_value=form_body_class)
        parse_multipart_body = mocker.patch.object(Endpoint, "parse_multipart_body", return_value=multipart_body_class)

        json_body = mocker.MagicMock(autospec=Property)
        json_body_imports = mocker.MagicMock()
        json_body.get_imports.return_value = {json_body_imports}
        parsed_schemas = mocker.MagicMock()
        parse_request_json_body = mocker.patch.object(
            Endpoint, "parse_request_json_body", return_value=(json_body, parsed_schemas)
        )
        import_string_from_class = mocker.patch(
            f"{MODULE_NAME}.import_string_from_class", side_effect=["import_1", "import_2"]
        )

        endpoint = self.make_endpoint()
        initial_schemas = mocker.MagicMock()

        (endpoint, response_schemas) = Endpoint._add_body(
            endpoint=endpoint,
            data=oai.Operation.construct(requestBody=request_body),
            schemas=initial_schemas,
            config=config,
        )

        assert response_schemas == parsed_schemas
        parse_request_form_body.assert_called_once_with(body=request_body, config=config)
        parse_request_json_body.assert_called_once_with(
            body=request_body, schemas=initial_schemas, parent_name="name", config=config
        )
        parse_multipart_body.assert_called_once_with(body=request_body, config=config)
        import_string_from_class.assert_has_calls(
            [
                mocker.call(form_body_class, prefix="...models"),
                mocker.call(multipart_body_class, prefix="...models"),
            ]
        )
        json_body.get_imports.assert_called_once_with(prefix="...")
        assert endpoint.relative_imports == {"import_1", "import_2", "import_3", json_body_imports}
        assert endpoint.json_body == json_body
        assert endpoint.form_body_class == form_body_class
        assert endpoint.multipart_body_class == multipart_body_class

    def test__add_responses_status_code_error(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint, Schemas

        schemas = Schemas()
        response_1_data = mocker.MagicMock()
        data = {
            "not_a_number": response_1_data,
        }
        endpoint = self.make_endpoint()
        parse_error = ParseError(data=mocker.MagicMock())
        response_from_data = mocker.patch(f"{MODULE_NAME}.response_from_data", return_value=(parse_error, schemas))
        config = MagicMock()

        response, schemas = Endpoint._add_responses(endpoint=endpoint, data=data, schemas=schemas, config=config)

        assert response.errors == [
            ParseError(
                detail=f"Invalid response status code not_a_number (not a number), response will be ommitted from generated client"
            )
        ]
        response_from_data.assert_not_called()

    def test__add_responses_error(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint, Schemas

        schemas = Schemas()
        response_1_data = mocker.MagicMock()
        response_2_data = mocker.MagicMock()
        data = {
            "200": response_1_data,
            "404": response_2_data,
        }
        endpoint = self.make_endpoint()
        parse_error = ParseError(data=mocker.MagicMock())
        response_from_data = mocker.patch(f"{MODULE_NAME}.response_from_data", return_value=(parse_error, schemas))
        config = MagicMock()

        response, schemas = Endpoint._add_responses(endpoint=endpoint, data=data, schemas=schemas, config=config)

        response_from_data.assert_has_calls(
            [
                mocker.call(status_code=200, data=response_1_data, schemas=schemas, parent_name="name", config=config),
                mocker.call(status_code=404, data=response_2_data, schemas=schemas, parent_name="name", config=config),
            ]
        )
        assert response.errors == [
            ParseError(
                detail=f"Cannot parse response for status code 200, response will be ommitted from generated client",
                data=parse_error.data,
            ),
            ParseError(
                detail=f"Cannot parse response for status code 404, response will be ommitted from generated client",
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
        endpoint = self.make_endpoint()
        schemas = mocker.MagicMock()
        schemas_1 = mocker.MagicMock()
        schemas_2 = mocker.MagicMock()
        response_1 = Response(
            status_code=200,
            source="source",
            prop=DateTimeProperty(name="datetime", required=True, nullable=False, default=None),
        )
        response_2 = Response(
            status_code=404,
            source="source",
            prop=DateProperty(name="date", required=True, nullable=False, default=None),
        )
        response_from_data = mocker.patch(
            f"{MODULE_NAME}.response_from_data", side_effect=[(response_1, schemas_1), (response_2, schemas_2)]
        )
        config = MagicMock()

        endpoint, response_schemas = Endpoint._add_responses(
            endpoint=endpoint, data=data, schemas=schemas, config=config
        )

        response_from_data.assert_has_calls(
            [
                mocker.call(status_code=200, data=response_1_data, schemas=schemas, parent_name="name", config=config),
                mocker.call(
                    status_code=404, data=response_2_data, schemas=schemas_1, parent_name="name", config=config
                ),
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

        endpoint = self.make_endpoint()
        schemas = Schemas()
        config = MagicMock()

        # Just checking there's no exception here
        assert Endpoint._add_parameters(
            endpoint=endpoint, data=oai.Operation.construct(), schemas=schemas, config=config
        ) == (
            endpoint,
            schemas,
        )

    def test__add_parameters_parse_error(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint

        endpoint = self.make_endpoint()
        initial_schemas = mocker.MagicMock()
        parse_error = ParseError(data=mocker.MagicMock())
        property_schemas = mocker.MagicMock()
        mocker.patch(f"{MODULE_NAME}.property_from_data", return_value=(parse_error, property_schemas))
        param = oai.Parameter.construct(name="test", required=True, param_schema=mocker.MagicMock(), param_in="cookie")
        config = MagicMock()

        result = Endpoint._add_parameters(
            endpoint=endpoint, data=oai.Operation.construct(parameters=[param]), schemas=initial_schemas, config=config
        )
        assert result == (
            ParseError(data=parse_error.data, detail=f"cannot parse parameter of endpoint {endpoint.name}"),
            property_schemas,
        )

    def test__add_parameters_parse_error_on_non_required_path_param(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint, Schemas

        endpoint = self.make_endpoint()
        parsed_schemas = mocker.MagicMock()
        mocker.patch(f"{MODULE_NAME}.property_from_data", return_value=(mocker.MagicMock(), parsed_schemas))
        param = oai.Parameter.construct(
            name="test", required=False, param_schema=mocker.MagicMock(), param_in=oai.ParameterLocation.PATH
        )
        schemas = Schemas()
        config = MagicMock()

        result = Endpoint._add_parameters(
            endpoint=endpoint, data=oai.Operation.construct(parameters=[param]), schemas=schemas, config=config
        )
        assert result == (ParseError(data=param, detail="Path parameter must be required"), parsed_schemas)

    def test__add_parameters_fail_loudly_when_location_not_supported(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint, Schemas

        endpoint = self.make_endpoint()
        parsed_schemas = mocker.MagicMock()
        mocker.patch(f"{MODULE_NAME}.property_from_data", return_value=(mocker.MagicMock(), parsed_schemas))
        param = oai.Parameter.construct(
            name="test", required=True, param_schema=mocker.MagicMock(), param_in="error_location"
        )
        schemas = Schemas()
        config = MagicMock()

        result = Endpoint._add_parameters(
            endpoint=endpoint, data=oai.Operation.construct(parameters=[param]), schemas=schemas, config=config
        )
        assert result == (ParseError(data=param, detail="Parameter must be declared in path or query"), parsed_schemas)

    def test__add_parameters_happy(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint
        from openapi_python_client.parser.properties import Property

        endpoint = self.make_endpoint()
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
        config = MagicMock()

        (endpoint, schemas) = Endpoint._add_parameters(
            endpoint=endpoint, data=data, schemas=initial_schemas, config=config
        )

        property_from_data.assert_has_calls(
            [
                mocker.call(
                    name="path_prop_name",
                    required=True,
                    data=path_schema,
                    schemas=initial_schemas,
                    parent_name="name",
                    config=config,
                ),
                mocker.call(
                    name="query_prop_name",
                    required=False,
                    data=query_schema,
                    schemas=schemas_1,
                    parent_name="name",
                    config=config,
                ),
                mocker.call(
                    name="header_prop_name",
                    required=False,
                    data=header_schema,
                    schemas=schemas_2,
                    parent_name="name",
                    config=config,
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

    def test__add_parameters_duplicate_properties(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint, Schemas

        endpoint = self.make_endpoint()
        param = oai.Parameter.construct(
            name="test", required=True, param_schema=oai.Schema.construct(type="string"), param_in="path"
        )
        data = oai.Operation.construct(parameters=[param, param])
        schemas = Schemas()
        config = MagicMock()

        result = Endpoint._add_parameters(endpoint=endpoint, data=data, schemas=schemas, config=config)
        assert result == (
            ParseError(data=data, detail="Could not reconcile duplicate parameters named test_path"),
            schemas,
        )

    def test__add_parameters_duplicate_properties_different_location(self):
        from openapi_python_client.parser.openapi import Endpoint, Schemas

        endpoint = self.make_endpoint()
        path_param = oai.Parameter.construct(
            name="test", required=True, param_schema=oai.Schema.construct(type="string"), param_in="path"
        )
        query_param = oai.Parameter.construct(
            name="test", required=True, param_schema=oai.Schema.construct(type="string"), param_in="query"
        )
        schemas = Schemas()
        config = MagicMock()

        result = Endpoint._add_parameters(
            endpoint=endpoint,
            data=oai.Operation.construct(parameters=[path_param, query_param]),
            schemas=schemas,
            config=config,
        )[0]
        assert isinstance(result, Endpoint)
        assert result.path_parameters[0].python_name == "test_path"
        assert result.path_parameters[0].name == "test"
        assert result.query_parameters[0].python_name == "test_query"
        assert result.query_parameters[0].name == "test"

    def test__sort_parameters(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint

        endpoint = self.make_endpoint()
        path = "/multiple-path-parameters/{param4}/{param2}/{param1}/{param3}"

        for i in range(1, 5):
            param = oai.Parameter.construct(
                name=f"param{i}", required=True, param_schema=mocker.MagicMock(), param_in=oai.ParameterLocation.PATH
            )
            endpoint.path_parameters.append(param)

        result = Endpoint._sort_parameters(endpoint=endpoint, path=path)
        result_names = [p.name for p in result.path_parameters]
        expected_names = [f"param{i}" for i in (4, 2, 1, 3)]

        assert result_names == expected_names

    def test__sort_parameters_invalid_path_templating(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint

        endpoint = self.make_endpoint()
        path = "/multiple-path-parameters/{param1}/{param2}"
        param = oai.Parameter.construct(
            name="param1", required=True, param_schema=mocker.MagicMock(), param_in=oai.ParameterLocation.PATH
        )
        endpoint.path_parameters.append(param)

        result = Endpoint._sort_parameters(endpoint=endpoint, path=path)

        assert isinstance(result, ParseError)
        assert result.data == [param]
        assert "Incorrect path templating" in result.detail

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
        config = MagicMock()

        result = Endpoint.from_data(
            data=data, path=path, method=method, tag="default", schemas=inital_schemas, config=config
        )

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
        config = MagicMock()

        result = Endpoint.from_data(
            data=data, path=path, method=method, tag="default", schemas=initial_schemas, config=config
        )

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
        config = MagicMock()

        mocker.patch("openapi_python_client.utils.remove_string_escapes", return_value=data.description)

        endpoint = Endpoint.from_data(
            data=data, path=path, method=method, tag="default", schemas=initial_schemas, config=config
        )

        assert endpoint == _add_body.return_value

        _add_parameters.assert_called_once_with(
            endpoint=Endpoint(
                path=path,
                method=method,
                description=data.description,
                summary="",
                name=data.operationId,
                requires_security=True,
                tag="default",
            ),
            data=data,
            schemas=initial_schemas,
            config=config,
        )
        _add_responses.assert_called_once_with(
            endpoint=param_endpoint, data=data.responses, schemas=param_schemas, config=config
        )
        _add_body.assert_called_once_with(
            endpoint=response_endpoint, data=data, schemas=response_schemas, config=config
        )

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
        config = MagicMock()

        result = Endpoint.from_data(data=data, path=path, method=method, tag="default", schemas=schemas, config=config)

        assert result == _add_body.return_value

        _add_parameters.assert_called_once_with(
            endpoint=Endpoint(
                path=path,
                method=method,
                description=data.description,
                summary="",
                name="get_path_with_param",
                requires_security=True,
                tag="default",
            ),
            data=data,
            schemas=schemas,
            config=config,
        )
        _add_responses.assert_called_once_with(
            endpoint=_add_parameters.return_value[0],
            data=data.responses,
            schemas=_add_parameters.return_value[1],
            config=config,
        )
        _add_body.assert_called_once_with(
            endpoint=_add_responses.return_value[0], data=data, schemas=_add_responses.return_value[1], config=config
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
        config = MagicMock()

        Endpoint.from_data(data=data, path=path, method=method, tag="a", schemas=schemas, config=config)

        _add_parameters.assert_called_once_with(
            endpoint=Endpoint(
                path=path,
                method=method,
                description=data.description,
                summary="",
                name=data.operationId,
                requires_security=False,
                tag="a",
            ),
            data=data,
            schemas=schemas,
            config=config,
        )
        _add_responses.assert_called_once_with(
            endpoint=_add_parameters.return_value[0],
            data=data.responses,
            schemas=_add_parameters.return_value[1],
            config=config,
        )
        _add_body.assert_called_once_with(
            endpoint=_add_responses.return_value[0], data=data, schemas=_add_responses.return_value[1], config=config
        )

    @pytest.mark.parametrize(
        "response_types, expected",
        (([], "None"), (["Something"], "Something"), (["First", "Second", "Second"], "Union[First, Second]")),
    )
    def test_response_type(self, response_types, expected):
        endpoint = self.make_endpoint()
        for response_type in response_types:
            mock_response = MagicMock()
            mock_response.prop.get_type_string.return_value = response_type
            endpoint.responses.append(mock_response)

        assert endpoint.response_type() == expected


class TestImportStringFromReference:
    def test_import_string_from_reference_no_prefix(self, mocker):
        from openapi_python_client.parser.openapi import import_string_from_class
        from openapi_python_client.parser.properties import Class

        class_ = mocker.MagicMock(autospec=Class)
        result = import_string_from_class(class_)

        assert result == f"from .{class_.module_name} import {class_.name}"

    def test_import_string_from_reference_with_prefix(self, mocker):
        from openapi_python_client.parser.openapi import import_string_from_class
        from openapi_python_client.parser.properties import Class

        prefix = mocker.MagicMock(autospec=str)
        class_ = mocker.MagicMock(autospec=Class)
        result = import_string_from_class(class_=class_, prefix=prefix)

        assert result == f"from {prefix}.{class_.module_name} import {class_.name}"


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
        config = MagicMock()

        result = EndpointCollection.from_data(data=data, schemas=schemas, config=config)

        endpoint_from_data.assert_has_calls(
            [
                mocker.call(
                    data=path_1_put, path="path_1", method="put", tag="default", schemas=schemas, config=config
                ),
                mocker.call(
                    data=path_1_post, path="path_1", method="post", tag="tag_2", schemas=schemas_1, config=config
                ),
                mocker.call(
                    data=path_2_get, path="path_2", method="get", tag="default", schemas=schemas_2, config=config
                ),
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
        config = MagicMock()

        result, result_schemas = EndpointCollection.from_data(data=data, schemas=schemas, config=config)

        endpoint_from_data.assert_has_calls(
            [
                mocker.call(
                    data=path_1_put, path="path_1", method="put", tag="default", schemas=schemas, config=config
                ),
                mocker.call(
                    data=path_1_post, path="path_1", method="post", tag="tag_2", schemas=schemas_1, config=config
                ),
                mocker.call(
                    data=path_2_get, path="path_2", method="get", tag="default", schemas=schemas_2, config=config
                ),
            ],
        )
        assert result["default"].parse_errors[0].data == "1"
        assert result["default"].parse_errors[1].data == "3"
        assert result["tag_2"].parse_errors[0].data == "2"
        assert result_schemas == schemas_3

    def test_from_data_tags_snake_case_sanitizer(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint, EndpointCollection

        path_1_put = oai.Operation.construct()
        path_1_post = oai.Operation.construct(tags=["AMF Subscription Info (Document)", "tag_3"])
        path_2_get = oai.Operation.construct()
        data = {
            "path_1": oai.PathItem.construct(post=path_1_post, put=path_1_put),
            "path_2": oai.PathItem.construct(get=path_2_get),
        }
        endpoint_1 = mocker.MagicMock(autospec=Endpoint, tag="default", relative_imports={"1", "2"})
        endpoint_2 = mocker.MagicMock(autospec=Endpoint, tag="AMFSubscriptionInfo (Document)", relative_imports={"2"})
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
        config = MagicMock()

        result = EndpointCollection.from_data(data=data, schemas=schemas, config=config)

        endpoint_from_data.assert_has_calls(
            [
                mocker.call(
                    data=path_1_put, path="path_1", method="put", tag="default", schemas=schemas, config=config
                ),
                mocker.call(
                    data=path_1_post,
                    path="path_1",
                    method="post",
                    tag="amf_subscription_info_document",
                    schemas=schemas_1,
                    config=config,
                ),
                mocker.call(
                    data=path_2_get, path="path_2", method="get", tag="default", schemas=schemas_2, config=config
                ),
            ],
        )
        assert result == (
            {
                "default": EndpointCollection("default", endpoints=[endpoint_1, endpoint_3]),
                "amf_subscription_info_document": EndpointCollection(
                    "amf_subscription_info_document", endpoints=[endpoint_2]
                ),
            },
            schemas_3,
        )
