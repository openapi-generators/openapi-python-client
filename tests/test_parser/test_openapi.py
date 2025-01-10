from unittest.mock import MagicMock

import pydantic
import pytest

import openapi_python_client.schema as oai
from openapi_python_client.parser.errors import ParseError
from openapi_python_client.parser.openapi import Endpoint, EndpointCollection
from openapi_python_client.parser.properties import IntProperty, Parameters, Schemas
from openapi_python_client.schema import DataType

MODULE_NAME = "openapi_python_client.parser.openapi"


class TestEndpoint:
    def make_endpoint(self):
        from openapi_python_client.parser.openapi import Endpoint

        return Endpoint(
            path="path",
            method="method",
            description=None,
            name="name",
            requires_security=False,
            tags=["tag"],
            relative_imports={"import_3"},
        )

    @pytest.mark.parametrize("response_status_code", ["not_a_number", 499])
    def test__add_responses_status_code_error(self, response_status_code, mocker):
        from openapi_python_client.parser.openapi import Endpoint, Schemas

        schemas = Schemas()
        response_1_data = mocker.MagicMock()
        data = {
            response_status_code: response_1_data,
        }
        endpoint = self.make_endpoint()
        parse_error = ParseError(data=mocker.MagicMock())
        response_from_data = mocker.patch(f"{MODULE_NAME}.response_from_data", return_value=(parse_error, schemas))
        config = MagicMock()

        response, schemas = Endpoint._add_responses(
            endpoint=endpoint, data=data, schemas=schemas, responses={}, config=config
        )

        assert response.errors == [
            ParseError(
                detail=f"Invalid response status code {response_status_code} (not a valid HTTP status code), "
                "response will be omitted from generated client"
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
        parse_error = ParseError(data=mocker.MagicMock(), detail="some problem")
        response_from_data = mocker.patch(f"{MODULE_NAME}.response_from_data", return_value=(parse_error, schemas))
        config = MagicMock()

        response, schemas = Endpoint._add_responses(
            endpoint=endpoint, data=data, schemas=schemas, responses={}, config=config
        )

        response_from_data.assert_has_calls(
            [
                mocker.call(
                    status_code=200,
                    data=response_1_data,
                    schemas=schemas,
                    responses={},
                    parent_name="name",
                    config=config,
                ),
                mocker.call(
                    status_code=404,
                    data=response_2_data,
                    schemas=schemas,
                    responses={},
                    parent_name="name",
                    config=config,
                ),
            ]
        )
        assert response.errors == [
            ParseError(
                detail="Cannot parse response for status code 200 (some problem), "
                "response will be omitted from generated client",
                data=parse_error.data,
            ),
            ParseError(
                detail="Cannot parse response for status code 404 (some problem), "
                "response will be omitted from generated client",
                data=parse_error.data,
            ),
        ]

    def test_add_parameters_handles_no_params(self):
        from openapi_python_client.parser.openapi import Endpoint, Schemas

        endpoint = self.make_endpoint()
        schemas = Schemas()
        parameters = Parameters()
        config = MagicMock()

        # Just checking there's no exception here
        assert Endpoint.add_parameters(
            endpoint=endpoint,
            data=oai.Operation.model_construct(),
            schemas=schemas,
            parameters=parameters,
            config=config,
        ) == (endpoint, schemas, parameters)

    def test_add_parameters_parse_error(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint

        endpoint = self.make_endpoint()
        initial_schemas = mocker.MagicMock()
        initial_parameters = mocker.MagicMock()
        parse_error = ParseError(data=mocker.MagicMock())
        property_schemas = mocker.MagicMock()
        mocker.patch(f"{MODULE_NAME}.property_from_data", return_value=(parse_error, property_schemas))
        param = oai.Parameter.model_construct(
            name="test", required=True, param_schema=mocker.MagicMock(), param_in="cookie"
        )
        config = MagicMock()

        result, schemas, parameters = Endpoint.add_parameters(
            endpoint=endpoint,
            data=oai.Operation.model_construct(parameters=[param]),
            schemas=initial_schemas,
            parameters=initial_parameters,
            config=config,
        )
        assert (result, schemas, parameters) == (
            ParseError(
                data=parse_error.data,
                detail=f"cannot parse parameter of endpoint {endpoint.name}: {parse_error.detail}",
            ),
            initial_schemas,
            initial_parameters,
        )

    @pytest.mark.parametrize(
        "data_type, allowed",
        [
            (oai.DataType.STRING, True),
            (oai.DataType.INTEGER, True),
            (oai.DataType.NUMBER, True),
            (oai.DataType.BOOLEAN, True),
            (oai.DataType.ARRAY, False),
            (oai.DataType.OBJECT, False),
        ],
    )
    def test_add_parameters_header_types(self, data_type, allowed, config):
        from openapi_python_client.parser.openapi import Endpoint

        endpoint = self.make_endpoint()
        initial_schemas = Schemas()
        parameters = Parameters()
        param = oai.Parameter.model_construct(
            name="test", required=True, param_schema=oai.Schema(type=data_type), param_in=oai.ParameterLocation.HEADER
        )

        result = Endpoint.add_parameters(
            endpoint=endpoint,
            data=oai.Operation.model_construct(parameters=[param]),
            schemas=initial_schemas,
            parameters=parameters,
            config=config,
        )
        if allowed:
            assert isinstance(result[0], Endpoint)
        else:
            assert isinstance(result[0], ParseError)

    def test__add_parameters_parse_error_on_non_required_path_param(self, config):
        endpoint = self.make_endpoint()
        param = oai.Parameter.model_construct(
            name="test",
            required=False,
            param_schema=oai.Schema.model_construct(type="string"),
            param_in=oai.ParameterLocation.PATH,
        )
        schemas = Schemas()
        parameters = Parameters()

        result = Endpoint.add_parameters(
            endpoint=endpoint,
            data=oai.Operation.model_construct(parameters=[param]),
            parameters=parameters,
            schemas=schemas,
            config=config,
        )
        assert result == (ParseError(data=param, detail="Path parameter must be required"), schemas, parameters)

    def test_validation_error_when_location_not_supported(self, mocker):
        parsed_schemas = mocker.MagicMock()
        mocker.patch(f"{MODULE_NAME}.property_from_data", return_value=(mocker.MagicMock(), parsed_schemas))
        with pytest.raises(pydantic.ValidationError):
            oai.Parameter(name="test", required=True, param_schema=mocker.MagicMock(), param_in="error_location")

    def test__add_parameters_handles_invalid_references(self, config):
        """References are not supported as direct params yet"""
        endpoint = self.make_endpoint()
        data = oai.Operation.model_construct(
            parameters=[
                oai.Reference.model_construct(ref="blah"),
            ]
        )

        parameters = Parameters()
        (error, _, return_parameters) = endpoint.add_parameters(
            endpoint=endpoint, data=data, schemas=Schemas(), parameters=parameters, config=config
        )

        assert isinstance(error, ParseError)
        assert parameters == return_parameters

    def test__add_parameters_resolves_references(self, mocker, param_factory, config):
        """References are not supported as direct params yet"""
        endpoint = self.make_endpoint()
        data = oai.Operation.model_construct(
            parameters=[
                oai.Reference.model_construct(ref="#components/parameters/blah"),
            ]
        )

        parameters = mocker.MagicMock()
        new_param = param_factory(name="blah", schema=oai.Schema.model_construct(type="string"))
        parameters.classes_by_name = {
            "blah": new_param,
        }
        parameters.classes_by_reference = {"components/parameters/blah": new_param}

        (endpoint, _, return_parameters) = endpoint.add_parameters(
            endpoint=endpoint, data=data, schemas=Schemas(), parameters=parameters, config=config
        )

        assert isinstance(endpoint, Endpoint)
        assert parameters == return_parameters

    def test__add_parameters_skips_params_without_schemas(self, config):
        """Params without schemas are allowed per spec, but the any type doesn't make sense as a parameter"""
        endpoint = self.make_endpoint()
        data = oai.Operation.model_construct(
            parameters=[
                oai.Parameter.model_construct(
                    name="param",
                    param_in="path",
                ),
            ]
        )

        (endpoint, _, _) = endpoint.add_parameters(
            endpoint=endpoint, data=data, schemas=Schemas(), parameters=Parameters(), config=config
        )

        assert isinstance(endpoint, Endpoint)
        assert len(endpoint.path_parameters) == 0

    def test__add_parameters_same_identifier_conflict(self, config):
        endpoint = self.make_endpoint()
        data = oai.Operation.model_construct(
            parameters=[
                oai.Parameter.model_construct(
                    name="param",
                    param_in="path",
                    param_schema=oai.Schema.model_construct(type="string"),
                    required=True,
                ),
                oai.Parameter.model_construct(
                    name="param_path",
                    param_in="path",
                    param_schema=oai.Schema.model_construct(type="string"),
                    required=True,
                ),
                oai.Parameter.model_construct(
                    name="param",
                    param_in="query",
                    param_schema=oai.Schema.model_construct(type="string"),
                ),
            ]
        )

        (err, _, _) = endpoint.add_parameters(
            endpoint=endpoint, data=data, schemas=Schemas(), parameters=Parameters(), config=config
        )

        assert isinstance(err, ParseError)
        assert "param_path" in err.detail

    def test__add_parameters_query_optionality(self, config):
        endpoint = self.make_endpoint()
        data = oai.Operation.model_construct(
            parameters=[
                oai.Parameter.model_construct(
                    name="not_required",
                    required=False,
                    param_schema=oai.Schema.model_construct(type="string"),
                    param_in="query",
                ),
                oai.Parameter.model_construct(
                    name="required",
                    required=True,
                    param_schema=oai.Schema.model_construct(type="string"),
                    param_in="query",
                ),
            ]
        )

        (endpoint, _, _) = endpoint.add_parameters(
            endpoint=endpoint, data=data, schemas=Schemas(), parameters=Parameters(), config=config
        )

        assert len(endpoint.query_parameters) == 2, "Not all query params were added"
        for param in endpoint.query_parameters:
            if param.name == "required":
                assert param.required
            else:
                assert not param.required

    def test_add_parameters_duplicate_properties(self, config):
        from openapi_python_client.parser.openapi import Endpoint, Schemas

        endpoint = self.make_endpoint()
        param = oai.Parameter.model_construct(
            name="test", required=True, param_schema=oai.Schema.model_construct(type="string"), param_in="path"
        )
        data = oai.Operation.model_construct(parameters=[param, param])
        schemas = Schemas()
        parameters = Parameters()

        result = Endpoint.add_parameters(
            endpoint=endpoint, data=data, schemas=schemas, parameters=parameters, config=config
        )
        assert result == (
            ParseError(
                data=data,
                detail="Parameters MUST NOT contain duplicates. "
                "A unique parameter is defined by a combination of a name and location. "
                "Duplicated parameters named `test` detected in `path`.",
            ),
            schemas,
            parameters,
        )

    def test_add_parameters_duplicate_properties_different_location(self, config):
        from openapi_python_client.parser.openapi import Endpoint, Schemas

        endpoint = self.make_endpoint()
        path_param = oai.Parameter.model_construct(
            name="test", required=True, param_schema=oai.Schema.model_construct(type="string"), param_in="path"
        )
        query_param = oai.Parameter.model_construct(
            name="test", required=True, param_schema=oai.Schema.model_construct(type="string"), param_in="query"
        )
        schemas = Schemas()
        parameters = Parameters()

        result = Endpoint.add_parameters(
            endpoint=endpoint,
            data=oai.Operation.model_construct(parameters=[path_param, query_param]),
            schemas=schemas,
            parameters=parameters,
            config=config,
        )[0]
        assert isinstance(result, Endpoint)
        assert result.path_parameters[0].name == "test"
        assert result.query_parameters[0].name == "test"

    def test_sort_parameters(self, string_property_factory):
        from openapi_python_client.parser.openapi import Endpoint

        endpoint = self.make_endpoint()
        endpoint.path = "/multiple-path-parameters/{param4}/{param2}/{param1}/{param3}"

        for i in range(1, 5):
            prop = string_property_factory(name=f"param{i}")
            endpoint.path_parameters.append(prop)

        result = Endpoint.sort_parameters(endpoint=endpoint)
        result_names = [param.name for param in result.path_parameters]
        expected_names = [f"param{i}" for i in (4, 2, 1, 3)]

        assert result_names == expected_names

    def test_sort_parameters_missing_param(self, string_property_factory):
        from openapi_python_client.parser.openapi import Endpoint

        endpoint = self.make_endpoint()
        endpoint.path = "/multiple-path-parameters/{param1}/{param2}"
        param = string_property_factory(name="param1")
        endpoint.path_parameters.append(param)

        result = Endpoint.sort_parameters(endpoint=endpoint)

        assert isinstance(result, ParseError)
        assert "Incorrect path templating" in result.detail
        assert endpoint.path in result.detail

    def test_sort_parameters_extra_param(self, string_property_factory):
        from openapi_python_client.parser.openapi import Endpoint

        endpoint = self.make_endpoint()
        endpoint.path = "/multiple-path-parameters"
        param = string_property_factory(name="param1")
        endpoint.path_parameters.append(param)

        result = Endpoint.sort_parameters(endpoint=endpoint)

        assert isinstance(result, ParseError)
        assert "Incorrect path templating" in result.detail
        assert endpoint.path in result.detail

    def test_from_data_bad_params(self, mocker, config):
        from openapi_python_client.parser.openapi import Endpoint

        path = mocker.MagicMock()
        method = mocker.MagicMock()
        parse_error = ParseError(data=mocker.MagicMock())
        return_schemas = mocker.MagicMock()
        return_parameters = mocker.MagicMock()
        mocker.patch.object(Endpoint, "add_parameters", return_value=(parse_error, return_schemas, return_parameters))
        data = oai.Operation.model_construct(
            description=mocker.MagicMock(),
            operationId=mocker.MagicMock(),
            security={"blah": "bloo"},
            responses=mocker.MagicMock(),
        )
        initial_schemas = mocker.MagicMock()
        parameters = Parameters()

        result = Endpoint.from_data(
            data=data,
            path=path,
            method=method,
            tags=["default"],
            schemas=initial_schemas,
            responses={},
            parameters=parameters,
            config=config,
            request_bodies={},
        )

        assert result == (parse_error, return_schemas, return_parameters)

    def test_from_data_bad_responses(self, mocker, config):
        from openapi_python_client.parser.openapi import Endpoint

        path = mocker.MagicMock()
        method = mocker.MagicMock()
        parse_error = ParseError(data=mocker.MagicMock())
        param_schemas = mocker.MagicMock()
        return_parameters = mocker.MagicMock()
        mocker.patch.object(
            Endpoint, "add_parameters", return_value=(mocker.MagicMock(), param_schemas, return_parameters)
        )
        response_schemas = mocker.MagicMock()
        _add_responses = mocker.patch.object(Endpoint, "_add_responses", return_value=(parse_error, response_schemas))
        data = oai.Operation.model_construct(
            description=mocker.MagicMock(),
            operationId=mocker.MagicMock(),
            security={"blah": "bloo"},
            responses=mocker.MagicMock(),
        )
        initial_schemas = mocker.MagicMock()
        initial_parameters = mocker.MagicMock()

        result = Endpoint.from_data(
            data=data,
            path=path,
            method=method,
            tags=["default"],
            schemas=initial_schemas,
            responses={},
            parameters=initial_parameters,
            config=config,
            request_bodies={},
        )

        assert result == (parse_error, response_schemas, return_parameters)

    def test_from_data_standard(self, mocker, config):
        from openapi_python_client.parser.openapi import Endpoint

        path = mocker.MagicMock()
        method = mocker.MagicMock()
        param_schemas = mocker.MagicMock()
        param_endpoint = mocker.MagicMock()
        return_parameters = mocker.MagicMock()
        add_parameters = mocker.patch.object(
            Endpoint, "add_parameters", return_value=(param_endpoint, param_schemas, return_parameters)
        )
        response_schemas = mocker.MagicMock()
        response_endpoint = mocker.MagicMock()
        _add_responses = mocker.patch.object(
            Endpoint, "_add_responses", return_value=(response_endpoint, response_schemas)
        )
        data = oai.Operation.model_construct(
            description=mocker.MagicMock(),
            operationId=mocker.MagicMock(),
            security={"blah": "bloo"},
            responses=mocker.MagicMock(),
        )
        initial_schemas = mocker.MagicMock()
        initial_parameters = mocker.MagicMock()

        mocker.patch("openapi_python_client.utils.remove_string_escapes", return_value=data.description)

        Endpoint.from_data(
            data=data,
            path=path,
            method=method,
            tags=["default"],
            schemas=initial_schemas,
            responses={},
            parameters=initial_parameters,
            config=config,
            request_bodies={},
        )

        add_parameters.assert_called_once_with(
            endpoint=Endpoint(
                path=path,
                method=method,
                description=data.description,
                summary="",
                name=data.operationId,
                requires_security=True,
                tags=["default"],
            ),
            data=data,
            schemas=initial_schemas,
            parameters=initial_parameters,
            config=config,
        )
        _add_responses.assert_called_once_with(
            endpoint=param_endpoint, data=data.responses, schemas=param_schemas, responses={}, config=config
        )

    def test_from_data_no_operation_id(self, mocker, config):
        from openapi_python_client.parser.openapi import Endpoint

        path = "/path/with/{param}/"
        method = "get"
        add_parameters = mocker.patch.object(
            Endpoint, "add_parameters", return_value=(mocker.MagicMock(), mocker.MagicMock(), mocker.MagicMock())
        )
        _add_responses = mocker.patch.object(
            Endpoint, "_add_responses", return_value=(mocker.MagicMock(), mocker.MagicMock())
        )
        data = oai.Operation.model_construct(
            description=mocker.MagicMock(),
            operationId=None,
            security={"blah": "bloo"},
            responses=mocker.MagicMock(),
        )
        schemas = mocker.MagicMock()
        mocker.patch("openapi_python_client.utils.remove_string_escapes", return_value=data.description)
        parameters = mocker.MagicMock()

        endpoint, _, return_params = Endpoint.from_data(
            data=data,
            path=path,
            method=method,
            tags=["default"],
            schemas=schemas,
            responses={},
            parameters=parameters,
            config=config,
            request_bodies={},
        )

        add_parameters.assert_called_once_with(
            endpoint=Endpoint(
                path=path,
                method=method,
                description=data.description,
                summary="",
                name="get_path_with_param",
                requires_security=True,
                tags=["default"],
            ),
            data=data,
            schemas=schemas,
            config=config,
            parameters=parameters,
        )
        _add_responses.assert_called_once_with(
            endpoint=add_parameters.return_value[0],
            data=data.responses,
            schemas=add_parameters.return_value[1],
            responses={},
            config=config,
        )

    def test_from_data_no_security(self, mocker, config):
        from openapi_python_client.parser.openapi import Endpoint

        data = oai.Operation.model_construct(
            description=mocker.MagicMock(),
            operationId=mocker.MagicMock(),
            security=None,
            responses=mocker.MagicMock(),
        )
        add_parameters = mocker.patch.object(
            Endpoint, "add_parameters", return_value=(mocker.MagicMock(), mocker.MagicMock(), mocker.MagicMock())
        )
        _add_responses = mocker.patch.object(
            Endpoint, "_add_responses", return_value=(mocker.MagicMock(), mocker.MagicMock())
        )
        path = mocker.MagicMock()
        method = mocker.MagicMock()
        mocker.patch("openapi_python_client.utils.remove_string_escapes", return_value=data.description)
        schemas = mocker.MagicMock()
        parameters = mocker.MagicMock()

        Endpoint.from_data(
            data=data,
            path=path,
            method=method,
            tags=["a"],
            schemas=schemas,
            responses={},
            parameters=parameters,
            config=config,
            request_bodies={},
        )

        add_parameters.assert_called_once_with(
            endpoint=Endpoint(
                path=path,
                method=method,
                description=data.description,
                summary="",
                name=data.operationId,
                requires_security=False,
                tags=["a"],
            ),
            data=data,
            parameters=parameters,
            schemas=schemas,
            config=config,
        )
        _add_responses.assert_called_once_with(
            endpoint=add_parameters.return_value[0],
            data=data.responses,
            schemas=add_parameters.return_value[1],
            responses={},
            config=config,
        )

    def test_from_data_some_bad_bodies(self, config):
        endpoint, _, _ = Endpoint.from_data(
            data=oai.Operation(
                responses={},
                requestBody=oai.RequestBody(
                    content={
                        "application/json": oai.MediaType(media_type_schema=oai.Schema(type=DataType.STRING)),
                        "not a real media type": oai.MediaType(media_type_schema=oai.Schema(type=DataType.STRING)),
                    },
                ),
            ),
            schemas=Schemas(),
            responses={},
            config=config,
            parameters=Parameters(),
            tags=["tag"],
            path="/",
            method="get",
            request_bodies={},
        )

        assert isinstance(endpoint, Endpoint)
        assert len(endpoint.bodies) == 1
        assert len(endpoint.errors) == 1

    def test_from_data_all_bodies_bad(self, config):
        endpoint, _, _ = Endpoint.from_data(
            data=oai.Operation(
                responses={},
                requestBody=oai.RequestBody(
                    content={
                        "not a real media type": oai.MediaType(media_type_schema=oai.Schema(type=DataType.STRING)),
                    },
                ),
            ),
            schemas=Schemas(),
            responses={},
            config=config,
            parameters=Parameters(),
            tags=["tag"],
            path="/",
            method="get",
            request_bodies={},
        )

        assert isinstance(endpoint, ParseError)

    @pytest.mark.parametrize(
        "response_types, expected",
        (([], "Any"), (["Something"], "Something"), (["First", "Second", "Second"], "Union[First, Second]")),
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
    def test_from_data_overrides_path_item_params_with_operation_params(self, config):
        data = {
            "/": oai.PathItem.model_construct(
                parameters=[
                    oai.Parameter.model_construct(
                        name="param", param_in="query", param_schema=oai.Schema.model_construct(type="string")
                    ),
                ],
                get=oai.Operation.model_construct(
                    parameters=[
                        oai.Parameter.model_construct(
                            name="param", param_in="query", param_schema=oai.Schema.model_construct(type="integer")
                        )
                    ],
                    responses={"200": oai.Response.model_construct(description="blah")},
                ),
            )
        }

        collections, schemas, parameters = EndpointCollection.from_data(
            data=data,
            schemas=Schemas(),
            parameters=Parameters(),
            config=config,
            request_bodies={},
            responses={},
        )
        collection: EndpointCollection = collections["default"]
        assert isinstance(collection.endpoints[0].query_parameters[0], IntProperty)
