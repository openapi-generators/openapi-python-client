import pytest
from attr import evolve

from openapi_python_client.parser.errors import ParameterError
from openapi_python_client.parser.properties import Class, Parameters
from openapi_python_client.parser.properties.schemas import parameter_from_reference
from openapi_python_client.schema import Parameter, Reference
from openapi_python_client.utils import ClassName

MODULE_NAME = "openapi_python_client.parser.properties.schemas"


def test_class_from_string_default_config(config):
    from openapi_python_client.parser.properties import Class

    class_ = Class.from_string(string="#/components/schemas/PingResponse", config=config)

    assert class_.name == "PingResponse"
    assert class_.module_name == "ping_response"


@pytest.mark.parametrize(
    "class_override, module_override, expected_class, expected_module",
    (
        (None, None, "MyResponse", "my_response"),
        ("MyClass", None, "MyClass", "my_class"),
        ("MyClass", "some_module", "MyClass", "some_module"),
        (None, "some_module", "MyResponse", "some_module"),
    ),
)
def test_class_from_string(class_override, module_override, expected_class, expected_module, config):
    from openapi_python_client.config import ClassOverride
    from openapi_python_client.parser.properties import Class

    ref = "#/components/schemas/MyResponse"
    config = evolve(
        config, class_overrides={"MyResponse": ClassOverride(class_name=class_override, module_name=module_override)}
    )

    result = Class.from_string(string=ref, config=config)
    assert result.name == expected_class
    assert result.module_name == expected_module


class TestParameterFromData:
    def test_cannot_parse_parameters_by_reference(self, config):
        from openapi_python_client.parser.properties import Parameters
        from openapi_python_client.parser.properties.schemas import parameter_from_data

        ref = Reference.model_construct(ref="#/components/parameters/a_param")
        parameters = Parameters()
        param_or_error, new_parameters = parameter_from_data(
            name="a_param", data=ref, parameters=parameters, config=config
        )
        assert param_or_error == ParameterError("Unable to resolve another reference")
        assert new_parameters == parameters

    def test_parameters_without_schema_are_ignored(self, config):
        from openapi_python_client.parser.properties import Parameters
        from openapi_python_client.parser.properties.schemas import parameter_from_data
        from openapi_python_client.schema import ParameterLocation

        param = Parameter(name="a_schemaless_param", param_in=ParameterLocation.QUERY)
        parameters = Parameters()
        param_or_error, new_parameters = parameter_from_data(
            name=param.name, data=param, parameters=parameters, config=config
        )
        assert param_or_error == ParameterError("Parameter has no schema")
        assert new_parameters == parameters

    def test_registers_new_parameters(self, config):
        from openapi_python_client.parser.properties import Parameters
        from openapi_python_client.parser.properties.schemas import parameter_from_data
        from openapi_python_client.schema import ParameterLocation, Schema

        param = Parameter.model_construct(
            name="a_param", param_in=ParameterLocation.QUERY, param_schema=Schema.model_construct()
        )
        parameters = Parameters()
        param_or_error, new_parameters = parameter_from_data(
            name=param.name, data=param, parameters=parameters, config=config
        )
        assert param_or_error == param
        assert new_parameters.classes_by_name[ClassName(param.name, prefix=config.field_prefix)] == param


class TestParameterFromReference:
    def test_returns_parameter_if_parameter_provided(self):
        param = Parameter.model_construct()
        params = Parameters()
        param_or_error = parameter_from_reference(param=param, parameters=params)
        assert param_or_error == param

    def test_errors_out_if_reference_not_in_parameters(self):
        ref = Reference.model_construct(ref="#/components/parameters/a_param")
        class_info = Class(name="a_param", module_name="module_name")
        existing_param = Parameter.model_construct(name="a_param")
        param_by_ref = Reference.model_construct(ref="#/components/parameters/another_param")
        params = Parameters(
            classes_by_name={class_info.name: existing_param}, classes_by_reference={ref.ref: existing_param}
        )
        param_or_error = parameter_from_reference(param=param_by_ref, parameters=params)
        assert param_or_error == ParameterError(
            detail="Reference `/components/parameters/another_param` not found.",
        )

    def test_returns_reference_from_registry(self):
        existing_param = Parameter.model_construct(name="a_param")
        class_info = Class(name="MyParameter", module_name="module_name")
        params = Parameters(
            classes_by_name={class_info.name: existing_param},
            classes_by_reference={"/components/parameters/a_param": existing_param},
        )

        param_by_ref = Reference.model_construct(ref="#/components/parameters/a_param")
        param_or_error = parameter_from_reference(param=param_by_ref, parameters=params)
        assert param_or_error == existing_param


class TestUpdateParametersFromData:
    def test_reports_parameters_with_errors(self, mocker, config):
        from openapi_python_client.parser.properties.schemas import update_parameters_with_data
        from openapi_python_client.schema import ParameterLocation, Schema

        parameters = Parameters()
        param = Parameter.model_construct(
            name="a_param", param_in=ParameterLocation.QUERY, param_schema=Schema.model_construct()
        )
        parameter_from_data = mocker.patch(
            f"{MODULE_NAME}.parameter_from_data", side_effect=[(ParameterError(), parameters)]
        )
        ref_path = Reference.model_construct(ref="#/components/parameters/a_param")
        new_parameters_or_error = update_parameters_with_data(
            ref_path=ref_path.ref, data=param, parameters=parameters, config=config
        )

        parameter_from_data.assert_called_once()
        assert new_parameters_or_error == ParameterError(
            detail="Unable to parse this part of your OpenAPI document: : None",
            header="Unable to parse parameter #/components/parameters/a_param",
        )

    def test_records_references_to_parameters(self, mocker, config):
        from openapi_python_client.parser.properties.schemas import update_parameters_with_data
        from openapi_python_client.schema import ParameterLocation, Schema

        parameters = Parameters()
        param = Parameter.model_construct(
            name="a_param", param_in=ParameterLocation.QUERY, param_schema=Schema.model_construct()
        )
        parameter_from_data = mocker.patch(f"{MODULE_NAME}.parameter_from_data", side_effect=[(param, parameters)])
        ref_path = "#/components/parameters/a_param"
        new_parameters = update_parameters_with_data(
            ref_path=ref_path, data=param, parameters=parameters, config=config
        )

        parameter_from_data.assert_called_once()
        assert new_parameters.classes_by_reference[ref_path] == param
