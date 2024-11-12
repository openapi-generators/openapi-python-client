from typing import Any, Dict
import re
from typing import List, Optional

from click.testing import Result
import pytest

from end_to_end_tests.generated_client import generate_client_from_inline_spec, GeneratedClientContext


def with_generated_client_fixture(
    openapi_spec: str,
    name: str="generated_client",
    config: str="",
    extra_args: List[str] = [],
):
    """Decorator to apply to a test class to create a fixture inside it called 'generated_client'.
    
    The fixture value will be a GeneratedClientContext created by calling
    generate_client_from_inline_spec().
    """
    def _decorator(cls):
        def generated_client(self):
            with generate_client_from_inline_spec(openapi_spec, extra_args=extra_args, config=config) as g:
                print(g.generator_result.stdout)  # so we'll see the output if a test failed
                yield g

        setattr(cls, name, pytest.fixture(scope="class")(generated_client))
        return cls

    return _decorator


def with_generated_code_import(import_path: str, alias: Optional[str] = None):
    """Decorator to apply to a test class to create a fixture from a generated code import.
    
    The 'generated_client' fixture must also be present.

    If import_path is "a.b.c", then the fixture's value is equal to "from a.b import c", and
    its name is "c" unless you specify a different name with the alias parameter.
    """
    parts = import_path.split(".")
    module_name = ".".join(parts[0:-1])
    import_name = parts[-1]

    def _decorator(cls):
        nonlocal alias

        def _func(self, generated_client):
            module = generated_client.import_module(module_name)
            return getattr(module, import_name)
        
        alias = alias or import_name
        _func.__name__ = alias
        setattr(cls, alias, pytest.fixture(scope="class")(_func))
        return cls
    
    return _decorator


def with_generated_code_imports(*import_paths: str):
    def _decorator(cls):
        decorated = cls
        for import_path in import_paths:
            decorated = with_generated_code_import(import_path)(decorated)
        return decorated

    return _decorator


def assert_model_decode_encode(model_class: Any, json_data: dict, expected_instance: Any) -> None:
    instance = model_class.from_dict(json_data)
    assert instance == expected_instance
    assert instance.to_dict() == json_data


def assert_model_property_type_hint(model_class: Any, name: str, expected_type_hint: Any) -> None:
    assert model_class.__annotations__[name] == expected_type_hint


def inline_spec_should_fail(
    openapi_spec: str,
    extra_args: List[str] = [],
    config: str = "",
    add_missing_sections = True,
) -> Result:
    """Asserts that the generator could not process the spec.
    
    Returns the command result, which could include stdout data or an exception.
    """
    with generate_client_from_inline_spec(
        openapi_spec, extra_args, config, add_missing_sections=add_missing_sections, raise_on_error=False
    ) as generated_client:
        assert generated_client.generator_result.exit_code != 0
        return generated_client.generator_result


def assert_bad_schema(
    generated_client: GeneratedClientContext,
    schema_name: str,
    expected_message_str: str,
) -> None:
    warnings = _GeneratorWarningsParser(generated_client)
    assert schema_name in warnings.by_schema, f"Did not find warning for schema {schema_name} in output: {warnings.output}"
    assert expected_message_str in warnings.by_schema[schema_name]


class _GeneratorWarningsParser:
    output: str
    by_schema: Dict[str, str]

    def __init__(self, generated_client: GeneratedClientContext) -> None:
        """Runs the generator, asserts that it printed warnings, and parses the warnings."""

        assert generated_client.generator_result.exit_code == 0
        output = generated_client.generator_result.stdout
        assert "Warning(s) encountered while generating" in output
        self.by_schema = {}
        self.output = output
        bad_schema_regex = "Unable to (parse|process) schema /components/schemas/(\w*)"
        last_name = ""
        while True:
            if not (match := re.search(bad_schema_regex, output)):
                break
            if last_name:
                self.by_schema[last_name] = output[0:match.start()]
            output = output[match.end():]
            last_name = match.group(2)
        if last_name:
            self.by_schema[last_name] = output
