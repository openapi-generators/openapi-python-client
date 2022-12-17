from unittest.mock import MagicMock

import pydantic
import pytest

import openapi_python_client.schema as oai
from openapi_python_client import Config, GeneratorError
from openapi_python_client.parser.errors import ParseError
from openapi_python_client.parser.openapi import Endpoint, EndpointCollection
from openapi_python_client.parser.properties import IntProperty, Parameters, Schemas
from openapi_python_client.schema import ParameterLocation

MODULE_NAME = "openapi_python_client.parser.openapi"


class TestGeneratorData:
    def test_from_dict(self, mocker, model_property_factory, enum_property_factory):
        from openapi_python_client.parser.properties import Schemas

        build_schemas = mocker.patch(f"{MODULE_NAME}.build_schemas")
        build_parameters = mocker.patch(f"{MODULE_NAME}.build_parameters")
        EndpointCollection = mocker.patch(f"{MODULE_NAME}.EndpointCollection")
        schemas = mocker.MagicMock()
        schemas.classes_by_name = {
            "Model": model_property_factory(),
            "Enum": enum_property_factory(),
        }
        parameters = Parameters()

        endpoints_collections_by_tag = mocker.MagicMock()
        EndpointCollection.from_data.return_value = (endpoints_collections_by_tag, schemas, parameters)
        OpenAPI = mocker.patch(f"{MODULE_NAME}.oai.OpenAPI")
        openapi = OpenAPI.parse_obj.return_value
        openapi.openapi = mocker.MagicMock(major=3)
        config = mocker.MagicMock()
        in_dict = mocker.MagicMock()

        from openapi_python_client.parser.openapi import GeneratorData

        generator_data = GeneratorData.from_dict(in_dict, config=config)

        OpenAPI.parse_obj.assert_called_once_with(in_dict)
        build_schemas.assert_called_once_with(components=openapi.components.schemas, config=config, schemas=Schemas())
        build_parameters.assert_called_once_with(
            components=openapi.components.parameters,
            parameters=parameters,
        )
        EndpointCollection.from_data.assert_called_once_with(
            data=openapi.paths,
            schemas=build_schemas.return_value,
            parameters=build_parameters.return_value,
            config=config,
        )
        assert generator_data.title == openapi.info.title
        assert generator_data.description == openapi.info.description
        assert generator_data.version == openapi.info.version
        assert generator_data.endpoint_collections_by_tag == endpoints_collections_by_tag
        assert generator_data.errors == schemas.errors + parameters.errors
        assert list(generator_data.models) == [schemas.classes_by_name["Model"]]
        assert list(generator_data.enums) == [schemas.classes_by_name["Enum"]]

        # Test no components
        openapi.components = None
        build_schemas.reset_mock()
        build_parameters.reset_mock()

        GeneratorData.from_dict(in_dict, config=config)

        build_schemas.assert_not_called()
        build_parameters.assert_not_called()

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

    def test_parse_request_form_body(self, mocker, model_property_factory):
        from openapi_python_client.parser.properties import Class

        schema = oai.Reference.construct(ref=mocker.MagicMock())
        body = oai.RequestBody.construct(
            content={"application/x-www-form-urlencoded": oai.MediaType.construct(media_type_schema=schema)}
        )
        class_info = Class(name="class_name", module_name="module_name")
        prop_before = model_property_factory(class_info=class_info)
        schemas_before = Schemas()
        property_from_data = mocker.patch(
            f"{MODULE_NAME}.property_from_data", return_value=(prop_before, schemas_before)
        )
        config = mocker.MagicMock()

        from openapi_python_client.parser.openapi import Endpoint

        result = Endpoint.parse_request_form_body(body=body, schemas=schemas_before, parent_name="name", config=config)

        property_from_data.assert_called_once_with(
            name="data", required=True, data=schema, schemas=schemas_before, parent_name="name", config=config
        )
        prop_after = model_property_factory(class_info=class_info)
        schemas_after = Schemas(classes_by_name={class_info.name: prop_after})
        assert result == (prop_after, schemas_after)

    def test_parse_request_form_body_no_data(self):
        body = oai.RequestBody.construct(content={})
        config = MagicMock()
        schemas = MagicMock()

        from openapi_python_client.parser.openapi import Endpoint

        result = Endpoint.parse_request_form_body(body=body, schemas=schemas, parent_name="name", config=config)

        assert result == (None, schemas)

    def test_parse_multipart_body(self, mocker, model_property_factory):
        from openapi_python_client.parser.openapi import Endpoint, Schemas
        from openapi_python_client.parser.properties import Class

        class_info = Class(name="class_name", module_name="module_name")
        prop_before = model_property_factory(class_info=class_info, is_multipart_body=False)

        schema = mocker.MagicMock()
        body = oai.RequestBody.construct(
            content={"multipart/form-data": oai.MediaType.construct(media_type_schema=schema)}
        )
        schemas_before = Schemas()
        config = MagicMock()
        property_from_data = mocker.patch(
            f"{MODULE_NAME}.property_from_data", return_value=(prop_before, schemas_before)
        )

        result = Endpoint.parse_multipart_body(body=body, schemas=schemas_before, parent_name="parent", config=config)

        property_from_data.assert_called_once_with(
            name="multipart_data",
            required=True,
            data=schema,
            schemas=schemas_before,
            parent_name="parent",
            config=config,
        )
        prop_after = model_property_factory(class_info=class_info, is_multipart_body=True)
        schemas_after = Schemas(classes_by_name={class_info.name: prop_after})
        assert result == (prop_after, schemas_after)

    def test_parse_multipart_body_existing_schema(self, mocker, model_property_factory):
        from openapi_python_client.parser.openapi import Endpoint, Schemas
        from openapi_python_client.parser.properties import Class

        class_info = Class(name="class_name", module_name="module_name")
        prop_before = model_property_factory(class_info=class_info, is_multipart_body=False)
        schemas_before = Schemas(classes_by_name={class_info.name: prop_before})

        schema = mocker.MagicMock()
        body = oai.RequestBody.construct(
            content={"multipart/form-data": oai.MediaType.construct(media_type_schema=schema)}
        )
        config = MagicMock()
        property_from_data = mocker.patch(
            f"{MODULE_NAME}.property_from_data", return_value=(prop_before, schemas_before)
        )

        result = Endpoint.parse_multipart_body(body=body, schemas=schemas_before, parent_name="parent", config=config)

        property_from_data.assert_called_once_with(
            name="multipart_data",
            required=True,
            data=schema,
            schemas=schemas_before,
            parent_name="parent",
            config=config,
        )
        prop_after = model_property_factory(class_info=class_info, is_multipart_body=True)
        schemas_after = Schemas(classes_by_name={class_info.name: prop_after})
        assert result == (prop_after, schemas_after)

    def test_parse_multipart_body_no_data(self):
        from openapi_python_client.parser.openapi import Endpoint, Schemas

        body = oai.RequestBody.construct(content={})
        schemas = Schemas()

        prop, schemas = Endpoint.parse_multipart_body(
            body=body, schemas=schemas, parent_name="parent", config=MagicMock()
        )

        assert prop is None

    @pytest.mark.parametrize(
        "content_type", ("application/json", "application/vnd.api+json", "application/yang-data+json")
    )
    def test_parse_request_json_body(self, mocker, content_type):
        from openapi_python_client.parser.openapi import Endpoint, Schemas

        schema = mocker.MagicMock()
        body = oai.RequestBody.construct(content={content_type: oai.MediaType.construct(media_type_schema=schema)})
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

    def test_add_body_bad_json_data(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint, Schemas

        schemas = Schemas()
        mocker.patch.object(Endpoint, "parse_request_form_body", return_value=(None, schemas))
        parse_error = ParseError(data=mocker.MagicMock(), detail=mocker.MagicMock())
        other_schemas = mocker.MagicMock()
        mocker.patch.object(Endpoint, "parse_request_json_body", return_value=(parse_error, other_schemas))
        endpoint = self.make_endpoint()
        request_body = mocker.MagicMock()

        result = Endpoint._add_body(
            endpoint=endpoint,
            data=oai.Operation.construct(requestBody=request_body),
            schemas=schemas,
            config=MagicMock(),
        )

        assert result == (
            ParseError(
                header=f"Cannot parse JSON body of endpoint {endpoint.name}",
                detail=parse_error.detail,
                data=parse_error.data,
            ),
            other_schemas,
        )

    def test_add_body_bad_form_data(self, enum_property_factory):
        from openapi_python_client.parser.openapi import Endpoint, Schemas

        schemas = Schemas(
            errors=[ParseError(detail="existing error")],
        )
        endpoint = self.make_endpoint()
        bad_schema = oai.Schema.construct(type=oai.DataType.ARRAY)

        result = Endpoint._add_body(
            endpoint=endpoint,
            data=oai.Operation.construct(
                requestBody=oai.RequestBody.construct(
                    content={"application/x-www-form-urlencoded": oai.MediaType.construct(media_type_schema=bad_schema)}
                )
            ),
            schemas=schemas,
            config=Config(),
        )

        assert result == (
            ParseError(
                detail="type array must have items defined",
                header="Cannot parse form body of endpoint name",
                data=bad_schema,
            ),
            schemas,
        )

    def test_add_body_bad_multipart_data(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint, Schemas

        schemas = Schemas()
        mocker.patch.object(Endpoint, "parse_request_form_body", return_value=(None, schemas))
        mocker.patch.object(Endpoint, "parse_request_json_body", return_value=(mocker.MagicMock(), mocker.MagicMock()))
        parse_error = ParseError(data=mocker.MagicMock(), detail=mocker.MagicMock())
        other_schemas = mocker.MagicMock()
        mocker.patch.object(Endpoint, "parse_multipart_body", return_value=(parse_error, other_schemas))
        endpoint = self.make_endpoint()
        request_body = mocker.MagicMock()

        result = Endpoint._add_body(
            endpoint=endpoint,
            data=oai.Operation.construct(requestBody=request_body),
            schemas=schemas,
            config=MagicMock(),
        )

        assert result == (
            ParseError(
                header=f"Cannot parse multipart body of endpoint {endpoint.name}",
                detail=parse_error.detail,
                data=parse_error.data,
            ),
            other_schemas,
        )

    def test_add_body_happy(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint
        from openapi_python_client.parser.properties import Property

        request_body = mocker.MagicMock()
        config = mocker.MagicMock()

        form_body = mocker.MagicMock(autospec=Property)
        form_body_imports = mocker.MagicMock()
        form_body.get_imports.return_value = {form_body_imports}
        form_schemas = mocker.MagicMock()
        parse_request_form_body = mocker.patch.object(
            Endpoint, "parse_request_form_body", return_value=(form_body, form_schemas)
        )

        multipart_body = mocker.MagicMock(autospec=Property)
        multipart_body_imports = mocker.MagicMock()
        multipart_body.get_imports.return_value = {multipart_body_imports}
        multipart_schemas = mocker.MagicMock()
        parse_multipart_body = mocker.patch.object(
            Endpoint, "parse_multipart_body", return_value=(multipart_body, multipart_schemas)
        )

        json_body = mocker.MagicMock(autospec=Property)
        json_body_imports = mocker.MagicMock()
        json_body.get_imports.return_value = {json_body_imports}
        json_schemas = mocker.MagicMock()
        parse_request_json_body = mocker.patch.object(
            Endpoint, "parse_request_json_body", return_value=(json_body, json_schemas)
        )

        endpoint = self.make_endpoint()
        initial_schemas = mocker.MagicMock()

        (endpoint, response_schemas) = Endpoint._add_body(
            endpoint=endpoint,
            data=oai.Operation.construct(requestBody=request_body),
            schemas=initial_schemas,
            config=config,
        )

        assert response_schemas == multipart_schemas
        parse_request_form_body.assert_called_once_with(
            body=request_body, schemas=initial_schemas, parent_name="name", config=config
        )
        parse_request_json_body.assert_called_once_with(
            body=request_body, schemas=form_schemas, parent_name="name", config=config
        )
        parse_multipart_body.assert_called_once_with(
            body=request_body, schemas=json_schemas, parent_name="name", config=config
        )
        form_body.get_imports.assert_called_once_with(prefix="...")
        json_body.get_imports.assert_called_once_with(prefix="...")
        multipart_body.get_imports.assert_called_once_with(prefix="...")
        assert endpoint.relative_imports == {"import_3", form_body_imports, json_body_imports, multipart_body_imports}
        assert endpoint.json_body == json_body
        assert endpoint.form_body == form_body
        assert endpoint.multipart_body == multipart_body

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

        response, schemas = Endpoint._add_responses(endpoint=endpoint, data=data, schemas=schemas, config=config)

        assert response.errors == [
            ParseError(
                detail=f"Invalid response status code {response_status_code} (not a valid HTTP status code), response will be ommitted from generated client"
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

        response, schemas = Endpoint._add_responses(endpoint=endpoint, data=data, schemas=schemas, config=config)

        response_from_data.assert_has_calls(
            [
                mocker.call(status_code=200, data=response_1_data, schemas=schemas, parent_name="name", config=config),
                mocker.call(status_code=404, data=response_2_data, schemas=schemas, parent_name="name", config=config),
            ]
        )
        assert response.errors == [
            ParseError(
                detail=f"Cannot parse response for status code 200 (some problem), "
                "response will be ommitted from generated client",
                data=parse_error.data,
            ),
            ParseError(
                detail=f"Cannot parse response for status code 404 (some problem), "
                "response will be ommitted from generated client",
                data=parse_error.data,
            ),
        ]

    def test__add_responses(self, mocker, date_time_property_factory, date_property_factory):
        from openapi_python_client.parser.openapi import Endpoint, Response

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
            prop=date_time_property_factory(name="datetime"),
        )
        response_2 = Response(
            status_code=404,
            source="source",
            prop=date_property_factory(name="date"),
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

    def test_add_parameters_handles_no_params(self):
        from openapi_python_client.parser.openapi import Endpoint, Schemas

        endpoint = self.make_endpoint()
        schemas = Schemas()
        parameters = Parameters()
        config = MagicMock()

        # Just checking there's no exception here
        assert Endpoint.add_parameters(
            endpoint=endpoint, data=oai.Operation.construct(), schemas=schemas, parameters=parameters, config=config
        ) == (endpoint, schemas, parameters)

    def test_add_parameters_parse_error(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint

        endpoint = self.make_endpoint()
        initial_schemas = mocker.MagicMock()
        initial_parameters = mocker.MagicMock()
        parse_error = ParseError(data=mocker.MagicMock())
        property_schemas = mocker.MagicMock()
        mocker.patch(f"{MODULE_NAME}.property_from_data", return_value=(parse_error, property_schemas))
        param = oai.Parameter.construct(name="test", required=True, param_schema=mocker.MagicMock(), param_in="cookie")
        config = MagicMock()

        result, schemas, parameters = Endpoint.add_parameters(
            endpoint=endpoint,
            data=oai.Operation.construct(parameters=[param]),
            schemas=initial_schemas,
            parameters=initial_parameters,
            config=config,
        )
        assert (result, schemas, parameters) == (
            ParseError(data=parse_error.data, detail=f"cannot parse parameter of endpoint {endpoint.name}"),
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
    def test_add_parameters_header_types(self, data_type, allowed):
        from openapi_python_client.parser.openapi import Endpoint

        endpoint = self.make_endpoint()
        initial_schemas = Schemas()
        parameters = Parameters()
        param = oai.Parameter.construct(
            name="test", required=True, param_schema=oai.Schema(type=data_type), param_in=oai.ParameterLocation.HEADER
        )
        config = Config()

        result = Endpoint.add_parameters(
            endpoint=endpoint,
            data=oai.Operation.construct(parameters=[param]),
            schemas=initial_schemas,
            parameters=parameters,
            config=config,
        )
        if allowed:
            assert isinstance(result[0], Endpoint)
        else:
            assert isinstance(result[0], ParseError)

    def test__add_parameters_parse_error_on_non_required_path_param(self):
        endpoint = self.make_endpoint()
        param = oai.Parameter.construct(
            name="test",
            required=False,
            param_schema=oai.Schema.construct(type="string"),
            param_in=oai.ParameterLocation.PATH,
        )
        schemas = Schemas()
        parameters = Parameters()

        result = Endpoint.add_parameters(
            endpoint=endpoint,
            data=oai.Operation.construct(parameters=[param]),
            parameters=parameters,
            schemas=schemas,
            config=Config(),
        )
        assert result == (ParseError(data=param, detail="Path parameter must be required"), schemas, parameters)

    def test_validation_error_when_location_not_supported(self, mocker):
        parsed_schemas = mocker.MagicMock()
        mocker.patch(f"{MODULE_NAME}.property_from_data", return_value=(mocker.MagicMock(), parsed_schemas))
        with pytest.raises(pydantic.ValidationError):
            oai.Parameter(name="test", required=True, param_schema=mocker.MagicMock(), param_in="error_location")

    def test__add_parameters_with_location_postfix_conflict1(self, mocker, property_factory):
        """Checks when the PythonIdentifier of new parameter already used."""
        from openapi_python_client.parser.openapi import Endpoint

        endpoint = self.make_endpoint()

        path_prop_conflicted = property_factory(name="prop_name_path", required=True, nullable=False, default=None)
        query_prop = property_factory(name="prop_name", required=True, nullable=False, default=None)
        path_prop = property_factory(name="prop_name", required=True, nullable=False, default=None)

        schemas_1 = mocker.MagicMock()
        schemas_2 = mocker.MagicMock()
        schemas_3 = mocker.MagicMock()
        mocker.patch(
            f"{MODULE_NAME}.property_from_data",
            side_effect=[
                (path_prop_conflicted, schemas_1),
                (query_prop, schemas_2),
                (path_prop, schemas_3),
            ],
        )
        path_conflicted_schema = mocker.MagicMock()
        query_schema = mocker.MagicMock()
        path_schema = mocker.MagicMock()

        data = oai.Operation.construct(
            parameters=[
                oai.Parameter.construct(
                    name=path_prop_conflicted.name, required=True, param_schema=path_conflicted_schema, param_in="path"
                ),
                oai.Parameter.construct(
                    name=query_prop.name, required=False, param_schema=query_schema, param_in="query"
                ),
                oai.Parameter.construct(name=path_prop.name, required=True, param_schema=path_schema, param_in="path"),
                oai.Reference.construct(),  # Should be ignored
                oai.Parameter.construct(),  # Should be ignored
            ]
        )
        initial_schemas = mocker.MagicMock()
        parameters = mocker.MagicMock()
        config = MagicMock()

        result = Endpoint.add_parameters(
            endpoint=endpoint, data=data, schemas=initial_schemas, parameters=parameters, config=config
        )[0]
        assert isinstance(result, ParseError)
        assert result.detail == "Parameters with same Python identifier `prop_name_path` detected"

    def test__add_parameters_with_location_postfix_conflict2(self, mocker, property_factory):
        """Checks when an existing parameter has a conflicting PythonIdentifier after renaming."""
        from openapi_python_client.parser.openapi import Endpoint

        endpoint = self.make_endpoint()
        path_prop_conflicted = property_factory(name="prop_name_path", required=True, nullable=False, default=None)
        path_prop = property_factory(name="prop_name", required=True, nullable=False, default=None)
        query_prop = property_factory(name="prop_name", required=True, nullable=False, default=None)
        schemas_1 = mocker.MagicMock()
        schemas_2 = mocker.MagicMock()
        schemas_3 = mocker.MagicMock()
        property_from_data = mocker.patch(
            f"{MODULE_NAME}.property_from_data",
            side_effect=[
                (path_prop_conflicted, schemas_1),
                (path_prop, schemas_2),
                (query_prop, schemas_3),
            ],
        )
        path_conflicted_schema = mocker.MagicMock()
        path_schema = mocker.MagicMock()
        query_schema = mocker.MagicMock()

        data = oai.Operation.construct(
            parameters=[
                oai.Parameter.construct(
                    name=path_prop_conflicted.name, required=True, param_schema=path_conflicted_schema, param_in="path"
                ),
                oai.Parameter.construct(name=path_prop.name, required=True, param_schema=path_schema, param_in="path"),
                oai.Parameter.construct(
                    name=query_prop.name, required=False, param_schema=query_schema, param_in="query"
                ),
                oai.Reference.construct(),  # Should be ignored
                oai.Parameter.construct(),  # Should be ignored
            ]
        )
        initial_schemas = mocker.MagicMock()
        parameters = mocker.MagicMock()
        config = MagicMock()

        result = Endpoint.add_parameters(
            endpoint=endpoint, data=data, schemas=initial_schemas, parameters=parameters, config=config
        )[0]
        assert isinstance(result, ParseError)
        assert result.detail == "Parameters with same Python identifier `prop_name_path` detected"

    def test__add_parameters_handles_invalid_references(self):
        """References are not supported as direct params yet"""
        endpoint = self.make_endpoint()
        data = oai.Operation.construct(
            parameters=[
                oai.Reference.construct(ref="blah"),
            ]
        )

        parameters = Parameters()
        (error, _, return_parameters) = endpoint.add_parameters(
            endpoint=endpoint, data=data, schemas=Schemas(), parameters=parameters, config=Config()
        )

        assert isinstance(error, ParseError)
        assert parameters == return_parameters

    def test__add_parameters_resolves_references(self, mocker, param_factory):
        """References are not supported as direct params yet"""
        endpoint = self.make_endpoint()
        data = oai.Operation.construct(
            parameters=[
                oai.Reference.construct(ref="#components/parameters/blah"),
            ]
        )

        parameters = mocker.MagicMock()
        new_param = param_factory(name="blah", schema=oai.Schema.construct(nullable=False, type="string"))
        parameters.classes_by_name = {
            "blah": new_param,
        }
        parameters.classes_by_reference = {"components/parameters/blah": new_param}

        (endpoint, _, return_parameters) = endpoint.add_parameters(
            endpoint=endpoint, data=data, schemas=Schemas(), parameters=parameters, config=Config()
        )

        assert isinstance(endpoint, Endpoint)
        assert parameters == return_parameters

    def test__add_parameters_skips_params_without_schemas(self):
        """Params without schemas are allowed per spec, but the any type doesn't make sense as a parameter"""
        endpoint = self.make_endpoint()
        data = oai.Operation.construct(
            parameters=[
                oai.Parameter.construct(
                    name="param",
                    param_in="path",
                ),
            ]
        )

        (endpoint, _, _) = endpoint.add_parameters(
            endpoint=endpoint, data=data, schemas=Schemas(), parameters=Parameters(), config=Config()
        )

        assert isinstance(endpoint, Endpoint)
        assert len(endpoint.path_parameters) == 0

    def test__add_parameters_same_identifier_conflict(self):
        endpoint = self.make_endpoint()
        data = oai.Operation.construct(
            parameters=[
                oai.Parameter.construct(
                    name="param",
                    param_in="path",
                    param_schema=oai.Schema.construct(nullable=False, type="string"),
                    required=True,
                ),
                oai.Parameter.construct(
                    name="param_path",
                    param_in="path",
                    param_schema=oai.Schema.construct(nullable=False, type="string"),
                    required=True,
                ),
                oai.Parameter.construct(
                    name="param",
                    param_in="query",
                    param_schema=oai.Schema.construct(nullable=False, type="string"),
                ),
            ]
        )

        (err, _, _) = endpoint.add_parameters(
            endpoint=endpoint, data=data, schemas=Schemas(), parameters=Parameters(), config=Config()
        )

        assert isinstance(err, ParseError)
        assert "param_path" in err.detail

    def test__add_parameters_query_optionality(self):
        endpoint = self.make_endpoint()
        data = oai.Operation.construct(
            parameters=[
                oai.Parameter.construct(
                    name="not_null_not_required",
                    required=False,
                    param_schema=oai.Schema.construct(nullable=False, type="string"),
                    param_in="query",
                ),
                oai.Parameter.construct(
                    name="not_null_required",
                    required=True,
                    param_schema=oai.Schema.construct(nullable=False, type="string"),
                    param_in="query",
                ),
                oai.Parameter.construct(
                    name="null_not_required",
                    required=False,
                    param_schema=oai.Schema.construct(nullable=True, type="string"),
                    param_in="query",
                ),
                oai.Parameter.construct(
                    name="null_required",
                    required=True,
                    param_schema=oai.Schema.construct(nullable=True, type="string"),
                    param_in="query",
                ),
            ]
        )

        (endpoint, _, _) = endpoint.add_parameters(
            endpoint=endpoint, data=data, schemas=Schemas(), parameters=Parameters(), config=Config()
        )

        assert len(endpoint.query_parameters) == 4, "Not all query params were added"
        for param in endpoint.query_parameters.values():
            if param.name == "not_null_required":
                assert not param.nullable
                assert param.required
            else:
                assert param.nullable
                assert not param.required

    def test_add_parameters_duplicate_properties(self):
        from openapi_python_client.parser.openapi import Endpoint, Schemas

        endpoint = self.make_endpoint()
        param = oai.Parameter.construct(
            name="test", required=True, param_schema=oai.Schema.construct(type="string"), param_in="path"
        )
        data = oai.Operation.construct(parameters=[param, param])
        schemas = Schemas()
        parameters = Parameters()
        config = MagicMock()

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

    def test_add_parameters_duplicate_properties_different_location(self):
        from openapi_python_client.parser.openapi import Endpoint, Schemas

        endpoint = self.make_endpoint()
        path_param = oai.Parameter.construct(
            name="test", required=True, param_schema=oai.Schema.construct(type="string"), param_in="path"
        )
        query_param = oai.Parameter.construct(
            name="test", required=True, param_schema=oai.Schema.construct(type="string"), param_in="query"
        )
        schemas = Schemas()
        parameters = Parameters()
        config = MagicMock()

        result = Endpoint.add_parameters(
            endpoint=endpoint,
            data=oai.Operation.construct(parameters=[path_param, query_param]),
            schemas=schemas,
            parameters=parameters,
            config=config,
        )[0]
        assert isinstance(result, Endpoint)
        assert result.path_parameters["test"].name == "test"
        assert result.query_parameters["test"].name == "test"

    def test_sort_parameters(self, string_property_factory):
        from openapi_python_client.parser.openapi import Endpoint

        endpoint = self.make_endpoint()
        endpoint.path = "/multiple-path-parameters/{param4}/{param2}/{param1}/{param3}"

        for i in range(1, 5):
            prop = string_property_factory(name=f"param{i}")
            endpoint.path_parameters[prop.name] = prop

        result = Endpoint.sort_parameters(endpoint=endpoint)
        result_names = [name for name in result.path_parameters]
        expected_names = [f"param{i}" for i in (4, 2, 1, 3)]

        assert result_names == expected_names

    def test_sort_parameters_missing_param(self, string_property_factory):
        from openapi_python_client.parser.openapi import Endpoint

        endpoint = self.make_endpoint()
        endpoint.path = "/multiple-path-parameters/{param1}/{param2}"
        param = string_property_factory(name="param1")
        endpoint.path_parameters[param.name] = param

        result = Endpoint.sort_parameters(endpoint=endpoint)

        assert isinstance(result, ParseError)
        assert "Incorrect path templating" in result.detail
        assert endpoint.path in result.detail

    def test_sort_parameters_extra_param(self, string_property_factory):
        from openapi_python_client.parser.openapi import Endpoint

        endpoint = self.make_endpoint()
        endpoint.path = "/multiple-path-parameters"
        param = string_property_factory(name="param1")
        endpoint.path_parameters[param.name] = param

        result = Endpoint.sort_parameters(endpoint=endpoint)

        assert isinstance(result, ParseError)
        assert "Incorrect path templating" in result.detail
        assert endpoint.path in result.detail

    def test_from_data_bad_params(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint

        path = mocker.MagicMock()
        method = mocker.MagicMock()
        parse_error = ParseError(data=mocker.MagicMock())
        return_schemas = mocker.MagicMock()
        return_parameters = mocker.MagicMock()
        add_parameters = mocker.patch.object(
            Endpoint, "add_parameters", return_value=(parse_error, return_schemas, return_parameters)
        )
        data = oai.Operation.construct(
            description=mocker.MagicMock(),
            operationId=mocker.MagicMock(),
            security={"blah": "bloo"},
            responses=mocker.MagicMock(),
        )
        initial_schemas = mocker.MagicMock()
        parameters = Parameters()
        config = MagicMock()

        result = Endpoint.from_data(
            data=data,
            path=path,
            method=method,
            tag="default",
            schemas=initial_schemas,
            parameters=parameters,
            config=config,
        )

        assert result == (parse_error, return_schemas, return_parameters)

    def test_from_data_bad_responses(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint

        path = mocker.MagicMock()
        method = mocker.MagicMock()
        parse_error = ParseError(data=mocker.MagicMock())
        param_schemas = mocker.MagicMock()
        return_parameters = mocker.MagicMock()
        add_parameters = mocker.patch.object(
            Endpoint, "add_parameters", return_value=(mocker.MagicMock(), param_schemas, return_parameters)
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
        initial_parameters = mocker.MagicMock()
        config = MagicMock()

        result = Endpoint.from_data(
            data=data,
            path=path,
            method=method,
            tag="default",
            schemas=initial_schemas,
            parameters=initial_parameters,
            config=config,
        )

        assert result == (parse_error, response_schemas, return_parameters)

    def test_from_data_standard(self, mocker):
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
        initial_parameters = mocker.MagicMock()
        config = MagicMock()

        mocker.patch("openapi_python_client.utils.remove_string_escapes", return_value=data.description)

        endpoint = Endpoint.from_data(
            data=data,
            path=path,
            method=method,
            tag="default",
            schemas=initial_schemas,
            parameters=initial_parameters,
            config=config,
        )

        assert (endpoint[0], endpoint[1]) == _add_body.return_value

        add_parameters.assert_called_once_with(
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
            parameters=initial_parameters,
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
        add_parameters = mocker.patch.object(
            Endpoint, "add_parameters", return_value=(mocker.MagicMock(), mocker.MagicMock(), mocker.MagicMock())
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
        parameters = mocker.MagicMock()

        endpoint, return_schemas, return_params = Endpoint.from_data(
            data=data, path=path, method=method, tag="default", schemas=schemas, parameters=parameters, config=config
        )

        assert (endpoint, return_schemas) == _add_body.return_value

        add_parameters.assert_called_once_with(
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
            parameters=parameters,
        )
        _add_responses.assert_called_once_with(
            endpoint=add_parameters.return_value[0],
            data=data.responses,
            schemas=add_parameters.return_value[1],
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
        add_parameters = mocker.patch.object(
            Endpoint, "add_parameters", return_value=(mocker.MagicMock(), mocker.MagicMock(), mocker.MagicMock())
        )
        _add_responses = mocker.patch.object(
            Endpoint, "_add_responses", return_value=(mocker.MagicMock(), mocker.MagicMock())
        )
        _add_body = mocker.patch.object(Endpoint, "_add_body", return_value=(mocker.MagicMock(), mocker.MagicMock()))
        path = mocker.MagicMock()
        method = mocker.MagicMock()
        mocker.patch("openapi_python_client.utils.remove_string_escapes", return_value=data.description)
        schemas = mocker.MagicMock()
        parameters = mocker.MagicMock()
        config = MagicMock()

        Endpoint.from_data(
            data=data, path=path, method=method, tag="a", schemas=schemas, parameters=parameters, config=config
        )

        add_parameters.assert_called_once_with(
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
            parameters=parameters,
            schemas=schemas,
            config=config,
        )
        _add_responses.assert_called_once_with(
            endpoint=add_parameters.return_value[0],
            data=data.responses,
            schemas=add_parameters.return_value[1],
            config=config,
        )
        _add_body.assert_called_once_with(
            endpoint=_add_responses.return_value[0], data=data, schemas=_add_responses.return_value[1], config=config
        )

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
    def test_from_data(self, mocker):
        from openapi_python_client.parser.openapi import Endpoint, EndpointCollection

        path_1_put = oai.Operation.construct()
        path_1_post = oai.Operation.construct(tags=["tag_2", "tag_3"])
        path_2_get = oai.Operation.construct()
        data = {
            "path_1": oai.PathItem.construct(post=path_1_post, put=path_1_put),
            "path_2": oai.PathItem.construct(get=path_2_get),
        }
        endpoint_1 = mocker.MagicMock(autospec=Endpoint, tag="default", relative_imports={"1", "2"}, path="path_1")
        endpoint_2 = mocker.MagicMock(autospec=Endpoint, tag="tag_2", relative_imports={"2"}, path="path_1")
        endpoint_3 = mocker.MagicMock(autospec=Endpoint, tag="default", relative_imports={"2", "3"}, path="path_2")
        schemas_1 = mocker.MagicMock()
        schemas_2 = mocker.MagicMock()
        schemas_3 = mocker.MagicMock()
        parameters_1 = mocker.MagicMock()
        parameters_2 = mocker.MagicMock()
        parameters_3 = mocker.MagicMock()
        endpoint_from_data = mocker.patch.object(
            Endpoint,
            "from_data",
            side_effect=[
                (endpoint_1, schemas_1, parameters_1),
                (endpoint_2, schemas_2, parameters_2),
                (endpoint_3, schemas_3, parameters_3),
            ],
        )
        schemas = mocker.MagicMock()
        parameters = mocker.MagicMock()
        config = MagicMock()

        result = EndpointCollection.from_data(data=data, schemas=schemas, parameters=parameters, config=config)

        endpoint_from_data.assert_has_calls(
            [
                mocker.call(
                    data=path_1_put,
                    path="path_1",
                    method="put",
                    tag="default",
                    schemas=schemas,
                    parameters=parameters,
                    config=config,
                ),
                mocker.call(
                    data=path_1_post,
                    path="path_1",
                    method="post",
                    tag="tag_2",
                    schemas=schemas_1,
                    parameters=parameters_1,
                    config=config,
                ),
                mocker.call(
                    data=path_2_get,
                    path="path_2",
                    method="get",
                    tag="default",
                    schemas=schemas_2,
                    parameters=parameters_2,
                    config=config,
                ),
            ],
        )
        assert result == (
            {
                "default": EndpointCollection("default", endpoints=[endpoint_1, endpoint_3]),
                "tag_2": EndpointCollection("tag_2", endpoints=[endpoint_2]),
            },
            schemas_3,
            parameters_3,
        )

    def test_from_data_overrides_path_item_params_with_operation_params(self):
        data = {
            "/": oai.PathItem.construct(
                parameters=[
                    oai.Parameter.construct(
                        name="param", param_in="query", param_schema=oai.Schema.construct(type="string")
                    ),
                ],
                get=oai.Operation.construct(
                    parameters=[
                        oai.Parameter.construct(
                            name="param", param_in="query", param_schema=oai.Schema.construct(type="integer")
                        )
                    ],
                    responses={"200": oai.Response.construct(description="blah")},
                ),
            )
        }

        collections, schemas, parameters = EndpointCollection.from_data(
            data=data,
            schemas=Schemas(),
            parameters=Parameters(),
            config=Config(),
        )
        collection: EndpointCollection = collections["default"]
        assert isinstance(collection.endpoints[0].query_parameters["param"], IntProperty)

    def test_from_data_errors(self, mocker):
        from openapi_python_client.parser.openapi import ParseError

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
        parameters_1 = mocker.MagicMock()
        parameters_2 = mocker.MagicMock()
        parameters_3 = mocker.MagicMock()
        endpoint_from_data = mocker.patch.object(
            Endpoint,
            "from_data",
            side_effect=[
                (ParseError(data="1"), schemas_1, parameters_1),
                (ParseError(data="2"), schemas_2, parameters_2),
                (mocker.MagicMock(errors=[ParseError(data="3")], path="path_2"), schemas_3, parameters_3),
            ],
        )
        schemas = mocker.MagicMock()
        parameters = mocker.MagicMock()
        config = MagicMock()

        result, result_schemas, result_parameters = EndpointCollection.from_data(
            data=data, schemas=schemas, config=config, parameters=parameters
        )

        endpoint_from_data.assert_has_calls(
            [
                mocker.call(
                    data=path_1_put,
                    path="path_1",
                    method="put",
                    tag="default",
                    schemas=schemas,
                    parameters=parameters,
                    config=config,
                ),
                mocker.call(
                    data=path_1_post,
                    path="path_1",
                    method="post",
                    tag="tag_2",
                    schemas=schemas_1,
                    parameters=parameters_1,
                    config=config,
                ),
                mocker.call(
                    data=path_2_get,
                    path="path_2",
                    method="get",
                    tag="default",
                    schemas=schemas_2,
                    parameters=parameters_2,
                    config=config,
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
        path_2_get = oai.Operation.construct(tags=["3. ABC"])
        data = {
            "path_1": oai.PathItem.construct(post=path_1_post, put=path_1_put),
            "path_2": oai.PathItem.construct(get=path_2_get),
        }
        endpoint_1 = mocker.MagicMock(autospec=Endpoint, tag="default", relative_imports={"1", "2"}, path="path_1")
        endpoint_2 = mocker.MagicMock(
            autospec=Endpoint, tag="AMFSubscriptionInfo (Document)", relative_imports={"2"}, path="path_1"
        )
        endpoint_3 = mocker.MagicMock(autospec=Endpoint, tag="default", relative_imports={"2", "3"}, path="path_2")
        schemas_1 = mocker.MagicMock()
        schemas_2 = mocker.MagicMock()
        schemas_3 = mocker.MagicMock()
        parameters_1 = mocker.MagicMock()
        parameters_2 = mocker.MagicMock()
        parameters_3 = mocker.MagicMock()
        endpoint_from_data = mocker.patch.object(
            Endpoint,
            "from_data",
            side_effect=[
                (endpoint_1, schemas_1, parameters_1),
                (endpoint_2, schemas_2, parameters_2),
                (endpoint_3, schemas_3, parameters_3),
            ],
        )
        schemas = mocker.MagicMock()
        parameters = mocker.MagicMock()
        config = MagicMock()

        result = EndpointCollection.from_data(data=data, schemas=schemas, parameters=parameters, config=config)

        endpoint_from_data.assert_has_calls(
            [
                mocker.call(
                    data=path_1_put,
                    path="path_1",
                    method="put",
                    tag="default",
                    schemas=schemas,
                    parameters=parameters,
                    config=config,
                ),
                mocker.call(
                    data=path_1_post,
                    path="path_1",
                    method="post",
                    tag="amf_subscription_info_document",
                    schemas=schemas_1,
                    parameters=parameters_1,
                    config=config,
                ),
                mocker.call(
                    data=path_2_get,
                    path="path_2",
                    method="get",
                    tag="tag3_abc",
                    schemas=schemas_2,
                    parameters=parameters_2,
                    config=config,
                ),
            ],
        )
        assert result == (
            {
                "default": EndpointCollection("default", endpoints=[endpoint_1]),
                "amf_subscription_info_document": EndpointCollection(
                    "amf_subscription_info_document", endpoints=[endpoint_2]
                ),
                "tag3_abc": EndpointCollection("tag3_abc", endpoints=[endpoint_3]),
            },
            schemas_3,
            parameters_3,
        )
