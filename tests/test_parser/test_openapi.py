from unittest.mock import MagicMock

import pydantic
import pytest

import openapi_python_client.schema as oai
from openapi_python_client.parser.errors import ParseError
from openapi_python_client.parser.openapi import Endpoint, EndpointCollection, import_string_from_class
from openapi_python_client.parser.properties import Class, IntProperty, Parameters, Schemas
from openapi_python_client.schema import DataType
from openapi_python_client.schema.ref import Ref
from openapi_python_client.schema.untrusted_string import UntrustedString
from openapi_python_client.strings import PythonCode, PythonIdentifier

MODULE_NAME = "openapi_python_client.parser.openapi"


class TestEndpoint:
    def make_endpoint(self):
        return Endpoint(
            path=UntrustedString("path"),
            method="method",
            description=UntrustedString(""),
            name=PythonIdentifier("name", prefix=""),
            requires_security=False,
            tags=[PythonIdentifier("tag", prefix="")],
            relative_imports={"import_3"},
            summary=UntrustedString("summary"),
        )

    def test_add_parameters_handles_no_params(self):
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
        endpoint = self.make_endpoint()
        initial_schemas = Schemas()
        parameters = Parameters()
        param = oai.Parameter.model_construct(
            name=UntrustedString("test"),
            required=True,
            param_schema=oai.Schema(type=data_type),
            param_in=oai.ParameterLocation.HEADER,
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
            name=UntrustedString("test"),
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
                oai.Reference.model_construct(ref=Ref("blah")),
            ]
        )

        parameters = Parameters()
        (error, _, return_parameters) = endpoint.add_parameters(
            endpoint=endpoint, data=data, schemas=Schemas(), parameters=parameters, config=config
        )

        assert isinstance(error, ParseError)
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
                    name=UntrustedString("param"),
                    param_in="path",
                    param_schema=oai.Schema.model_construct(type="string"),
                    required=True,
                ),
                oai.Parameter.model_construct(
                    name=UntrustedString("param_path"),
                    param_in="path",
                    param_schema=oai.Schema.model_construct(type="string"),
                    required=True,
                ),
                oai.Parameter.model_construct(
                    name=UntrustedString("param"),
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
                    name=UntrustedString("not_required"),
                    required=False,
                    param_schema=oai.Schema.model_construct(type="string"),
                    param_in="query",
                ),
                oai.Parameter.model_construct(
                    name=UntrustedString("required"),
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
        endpoint = self.make_endpoint()
        param = oai.Parameter.model_construct(
            name=UntrustedString("test"),
            required=True,
            param_schema=oai.Schema.model_construct(type="string"),
            param_in="path",
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
        endpoint = self.make_endpoint()
        path_param = oai.Parameter.model_construct(
            name=UntrustedString("test"),
            required=True,
            param_schema=oai.Schema.model_construct(type="string"),
            param_in="path",
        )
        query_param = oai.Parameter.model_construct(
            name=UntrustedString("test"),
            required=True,
            param_schema=oai.Schema.model_construct(type="string"),
            param_in="query",
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
        endpoint = self.make_endpoint()
        endpoint.path = UntrustedString("/multiple-path-parameters/{param4}/{param2}/{param1}/{param3}")

        for i in range(1, 5):
            prop = string_property_factory(name=f"param{i}")
            endpoint.path_parameters.append(prop)

        result = Endpoint.sort_parameters(endpoint=endpoint)
        result_names = [param.name for param in result.path_parameters]
        expected_names = [f"param{i}" for i in (4, 2, 1, 3)]

        assert result_names == expected_names

    def test_sort_parameters_missing_param(self, string_property_factory):
        endpoint = self.make_endpoint()
        endpoint.path = UntrustedString("/multiple-path-parameters/{param1}/{param2}")
        param = string_property_factory(name="param1")
        endpoint.path_parameters.append(param)

        result = Endpoint.sort_parameters(endpoint=endpoint)

        assert isinstance(result, ParseError)
        assert "Incorrect path templating" in result.detail
        assert endpoint.path.get_untrusted_value() in result.detail

    def test_sort_parameters_extra_param(self, string_property_factory):
        endpoint = self.make_endpoint()
        endpoint.path = UntrustedString("/multiple-path-parameters")
        param = string_property_factory(name="param1")
        endpoint.path_parameters.append(param)

        result = Endpoint.sort_parameters(endpoint=endpoint)

        assert isinstance(result, ParseError)
        assert "Incorrect path templating" in result.detail
        assert endpoint.path.get_untrusted_value() in result.detail

    @pytest.mark.parametrize(
        ("security", "expected_requires_security"),
        [
            ([{}], False),
            ([{"apiKey": []}, {}], False),
            ([{"apiKey": []}], True),
        ],
    )
    def test_from_data_security_allows_anonymous_alternative(
        self,
        security,
        expected_requires_security,
        mocker,
        config,
    ):
        data = oai.Operation.model_construct(
            description=mocker.MagicMock(),
            operationId=mocker.MagicMock(),
            security=security,
            responses=mocker.MagicMock(),
        )
        add_parameters = mocker.patch.object(
            Endpoint, "add_parameters", return_value=(mocker.MagicMock(), mocker.MagicMock(), mocker.MagicMock())
        )
        mocker.patch.object(Endpoint, "_add_responses", return_value=(mocker.MagicMock(), mocker.MagicMock()))
        path = mocker.MagicMock()
        method = mocker.MagicMock()
        mocker.patch("openapi_python_client.utils.remove_string_escapes", return_value=data.description)

        Endpoint.from_data(
            data=data,
            path=path,
            method=method,
            tags=["default"],
            schemas=mocker.MagicMock(),
            responses={},
            parameters=mocker.MagicMock(),
            config=config,
            request_bodies={},
        )

        assert add_parameters.call_args.kwargs["endpoint"].requires_security is expected_requires_security

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
            path=UntrustedString("/"),
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
            path=UntrustedString("/"),
            method="get",
            request_bodies={},
        )

        assert isinstance(endpoint, ParseError)

    @pytest.mark.parametrize(
        "response_types, expected",
        (([], "Any"), (["Something"], "Something"), (["First", "Second", "Second"], "First | Second")),
    )
    def test_response_type(self, response_types, expected):
        endpoint = self.make_endpoint()
        for response_type in response_types:
            mock_response = MagicMock()
            mock_response.prop.get_type_string.return_value = PythonCode(response_type)
            endpoint.responses.patterns.append(mock_response)

        assert endpoint.response_type() == PythonCode(expected)


class TestImportStringFromReference:
    def test_import_string_from_reference_no_prefix(self, mocker):
        class_ = mocker.MagicMock(autospec=Class)
        result = import_string_from_class(class_)

        assert result == f"from .{class_.module_name} import {class_.name}"

    def test_import_string_from_reference_with_prefix(self, mocker):
        prefix = mocker.MagicMock(autospec=str)
        class_ = mocker.MagicMock(autospec=Class)
        result = import_string_from_class(class_=class_, prefix=prefix)

        assert result == f"from {prefix}.{class_.module_name} import {class_.name}"


class TestEndpointCollection:
    def test_from_data_overrides_path_item_params_with_operation_params(self, config):
        data = {
            UntrustedString("/"): oai.PathItem.model_construct(
                parameters=[
                    oai.Parameter.model_construct(
                        name=UntrustedString("param"),
                        param_in="query",
                        param_schema=oai.Schema.model_construct(type="string"),
                    ),
                ],
                get=oai.Operation.model_construct(
                    parameters=[
                        oai.Parameter.model_construct(
                            name=UntrustedString("param"),
                            param_in="query",
                            param_schema=oai.Schema.model_construct(type="integer"),
                        )
                    ],
                    responses={UntrustedString("200"): oai.Response.model_construct(description="blah")},
                ),
            )
        }

        collections, _schemas, _parameters = EndpointCollection.from_data(
            data=data,
            schemas=Schemas(),
            parameters=Parameters(),
            config=config,
            request_bodies={},
            responses={},
        )
        collection: EndpointCollection = collections["default"]
        assert isinstance(collection.endpoints[0].query_parameters[0], IntProperty)
