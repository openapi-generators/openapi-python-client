import pytest
from attr import evolve

from openapi_python_client.config import ClassOverride
from openapi_python_client.parser.errors import ParameterError
from openapi_python_client.parser.properties import Class, Parameters
from openapi_python_client.parser.properties.schemas import (
    ReferencePath,
    parameter_from_data,
    parameter_from_reference,
)
from openapi_python_client.schema import Parameter, ParameterLocation, Reference, Schema
from openapi_python_client.schema.ref import Ref
from openapi_python_client.schema.untrusted_string import UntrustedString
from openapi_python_client.strings import ClassName

MODULE_NAME = "openapi_python_client.parser.properties.schemas"


def test_class_from_string_default_config(config):
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
    ref = "#/components/schemas/MyResponse"
    config = evolve(
        config, class_overrides={"MyResponse": ClassOverride(class_name=class_override, module_name=module_override)}
    )

    result = Class.from_string(string=ref, config=config)
    assert result.name == expected_class
    assert result.module_name == expected_module


class TestParameterFromData:
    def test_cannot_parse_parameters_by_reference(self, config):
        ref = Reference.model_construct(ref="#/components/parameters/a_param")
        parameters = Parameters()
        param_or_error, new_parameters = parameter_from_data(
            name="a_param", data=ref, parameters=parameters, config=config
        )
        assert param_or_error == ParameterError("Unable to resolve another reference")
        assert new_parameters == parameters

    def test_parameters_without_schema_are_ignored(self, config):
        param = Parameter(name="a_schemaless_param", param_in=ParameterLocation.QUERY)
        parameters = Parameters()
        param_or_error, new_parameters = parameter_from_data(
            name=param.name, data=param, parameters=parameters, config=config
        )
        assert param_or_error == ParameterError("Parameter has no schema")
        assert new_parameters == parameters

    def test_registers_new_parameters(self, config):
        param = Parameter.model_construct(
            name=UntrustedString("a_param"), param_in=ParameterLocation.QUERY, param_schema=Schema.model_construct()
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
        ref = Reference.model_construct(ref=Ref("#/components/parameters/a_param"))
        class_info = Class(name=ClassName(UntrustedString("a_param"), prefix=""), module_name="module_name")
        existing_param = Parameter.model_construct(name="a_param")
        param_by_ref = Reference.model_construct(ref=Ref("#/components/parameters/another_param"))
        params = Parameters(
            classes_by_name={class_info.name: existing_param}, classes_by_reference={ref.ref: existing_param}
        )
        param_or_error = parameter_from_reference(param=param_by_ref, parameters=params)
        assert param_or_error == ParameterError(
            detail="Reference `/components/parameters/another_param` not found.",
        )

    def test_returns_reference_from_registry(self):
        existing_param = Parameter.model_construct(name="a_param")
        class_info = Class(name=ClassName(UntrustedString("MyParameter"), prefix=""), module_name="module_name")
        params = Parameters(
            classes_by_name={class_info.name: existing_param},
            classes_by_reference={ReferencePath(UntrustedString("/components/parameters/a_param")): existing_param},
        )

        param_by_ref = Reference.model_construct(ref=Ref("#/components/parameters/a_param"))
        param_or_error = parameter_from_reference(param=param_by_ref, parameters=params)
        assert param_or_error == existing_param
