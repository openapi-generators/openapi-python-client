from openapi_python_client.parser.properties import EnumProperty
from openapi_python_client.parser.properties.schemas import Class
from openapi_python_client.schema.untrusted_string import UntrustedString
from openapi_python_client.strings import ClassName, PythonIdentifier


def _class_info() -> Class:
    return Class(name=ClassName(UntrustedString("MyEnum"), ""), module_name=PythonIdentifier("my_enum", ""))


def test_values_from_list_escapes_or_strips_control_characters():
    """Values are embedded in double-quoted string literals; newlines and control characters must be escaped"""
    values = EnumProperty.values_from_list(["line\nbreak", "tab\there", "nul\x00byte"], _class_info(), [])

    assert values["LINEBREAK"] == "linebreak"
    assert values["TABHERE"] == "tab\\there"
    assert values["NULBYTE"] == "nulbyte"
    # Every value must be safe inside a "..." literal in generated source
    for value in values.values():
        assert all(ord(c) >= 0x20 for c in value), value


def test_values_from_list_sanitizes_keys_with_backslash():
    """A backslash in a value must not survive into the generated identifier"""
    values = EnumProperty.values_from_list(["one\\two"], _class_info(), [])

    assert list(values) == ["ONE_TWO"]
