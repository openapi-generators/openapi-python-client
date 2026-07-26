from __future__ import annotations

import pytest

from openapi_python_client.parser.properties import AnyProperty
from openapi_python_client.parser.properties.protocol import Value, convert_example
from openapi_python_client.schema.untrusted_string import UntrustedString
from openapi_python_client.strings import PythonCode


@pytest.mark.parametrize(
    "required,no_optional,json,expected",
    [
        (False, False, False, "TestType | Unset"),
        (False, True, False, "TestType"),
        (True, False, False, "TestType"),
        (True, True, False, "TestType"),
        (False, False, True, "str | Unset"),
        (False, True, True, "str"),
        (True, False, True, "str"),
        (True, True, True, "str"),
    ],
)
def test_get_type_string(any_property_factory, mocker, required, no_optional, json, expected):
    mocker.patch.object(AnyProperty, "_type_string", "TestType")
    mocker.patch.object(AnyProperty, "_json_type_string", "str")
    p = any_property_factory(required=required)
    assert p.get_type_string(no_optional=no_optional, json=json) == PythonCode(expected)


@pytest.mark.parametrize(
    "default,required,expected",
    [
        (None, False, "test: Any | Unset = UNSET"),
        (None, True, "test: Any"),
        ("Test", False, "test: Any | Unset = Test"),
        ("Test", True, "test: Any = Test"),
    ],
)
def test_to_string(default: str | None, required: bool, expected: str, any_property_factory):
    name = "test"
    p = any_property_factory(
        name=name, required=required, default=Value(PythonCode(default), default) if default is not None else None
    )

    assert p.to_string() == PythonCode(expected)


def test_get_imports(any_property_factory):
    p = any_property_factory()
    assert p.get_imports(prefix="") == set()

    p = any_property_factory(name="test", required=False, default=None)
    assert p.get_imports(prefix="") == {"from types import UNSET, Unset"}


def test_to_docstring_escapes_description_and_example(any_property_factory):
    """Descriptions and examples must not be able to break out of the docstring"""
    p = any_property_factory(
        description='Break out """ print("uh oh")',
        example='Example """ print("uh oh")',
    )

    doc = p.to_docstring()

    assert '"""' not in doc
    assert r'\"\"\" print("uh oh")' in doc


def test_to_docstring_escapes_type_string(any_property_factory, mocker):
    """A type string containing literal values (e.g. const) must not break out of the docstring"""
    mocker.patch.object(AnyProperty, "_type_string", 'Literal[\'"""\']')
    p = any_property_factory()

    doc = p.to_docstring()

    assert '"""' not in doc


def test_to_docstring_escapes_default(any_property_factory):
    """A default's python_code must not be able to break out of the docstring"""
    # python_code for the string default '"""' is the 5-char source: "\"\"\""
    p = any_property_factory(default=Value(python_code=PythonCode('"\\"\\"\\""'), raw_value='"""'))

    doc = p.to_docstring()

    # The raw triple-quote must not survive into the docstring text
    assert '"""' not in doc


def test_get_instance_type_string(any_property_factory):
    p = any_property_factory(required=False)
    assert p.get_instance_type_string() == PythonCode("Any")


class TestConvertExample:
    def test_none(self):
        assert convert_example(None) is None

    def test_untrusted_string_passes_through(self):
        example = UntrustedString("an example")
        assert convert_example(example) is example

    def test_string_is_wrapped(self):
        converted = convert_example("an example")
        assert isinstance(converted, UntrustedString)
        assert converted == "an example"

    def test_non_string_is_stringified(self):
        """OpenAPI examples can be any type; they only appear in docstrings so stringify them"""
        converted = convert_example({"a": 1})
        assert isinstance(converted, UntrustedString)
        assert converted == "{'a': 1}"

    def test_property_converts_example(self, any_property_factory):
        p = any_property_factory(example={"a": 1})
        assert p.example == "{'a': 1}"
