from __future__ import annotations

import pytest

from openapi_python_client.parser.properties import AnyProperty
from openapi_python_client.parser.properties.protocol import Value


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
    assert p.get_type_string(no_optional=no_optional, json=json) == expected


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
        name=name, required=required, default=Value(default, default) if default is not None else None
    )

    assert p.to_string() == expected


def test_get_imports(any_property_factory):
    p = any_property_factory()
    assert p.get_imports(prefix="") == set()

    p = any_property_factory(name="test", required=False, default=None)
    assert p.get_imports(prefix="") == {"from types import UNSET, Unset"}
