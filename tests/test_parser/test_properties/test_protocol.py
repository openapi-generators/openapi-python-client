import pytest


def test_is_base_type(any_property_factory):
    assert any_property_factory().is_base_type is True


@pytest.mark.parametrize(
    "required,no_optional,json,quoted,expected",
    [
        (False, False, False, False, "Union[Unset, TestType]"),
        (False, True, False, False, "TestType"),
        (True, False, False, False, "TestType"),
        (True, True, False, False, "TestType"),
        (False, False, True, False, "Union[Unset, str]"),
        (False, True, True, False, "str"),
        (True, False, True, False, "str"),
        (True, True, True, False, "str"),
    ],
)
def test_get_type_string(any_property_factory, mocker, required, no_optional, json, expected, quoted):
    from openapi_python_client.parser.properties import AnyProperty

    mocker.patch.object(AnyProperty, "_type_string", "TestType")
    mocker.patch.object(AnyProperty, "_json_type_string", "str")
    p = any_property_factory(required=required)
    assert p.get_type_string(no_optional=no_optional, json=json, quoted=quoted) == expected


@pytest.mark.parametrize(
    "default,required,expected",
    [
        (None, False, "test: Union[Unset, TestType] = UNSET"),
        (None, True, "test: TestType"),
        ("Test", False, "test: Union[Unset, TestType] = Test"),
        ("Test", True, "test: TestType = Test"),
    ],
)
def test_to_string(mocker, default, required, expected, any_property_factory):
    name = "test"
    mocker.patch("openapi_python_client.parser.properties.AnyProperty._type_string", "TestType")
    p = any_property_factory(name=name, required=required, default=default)

    assert p.to_string() == expected


def test_get_imports(any_property_factory):
    p = any_property_factory()
    assert p.get_imports(prefix="") == set()

    p = any_property_factory(name="test", required=False, default=None)
    assert p.get_imports(prefix="") == {"from types import UNSET, Unset", "from typing import Union"}


@pytest.mark.parametrize(
    "quoted,expected",
    [
        (False, "TestType"),
        (True, "TestType"),
    ],
)
def test_get_base_type_string(quoted, expected, any_property_factory, mocker):
    from openapi_python_client.parser.properties import AnyProperty

    mocker.patch.object(AnyProperty, "_type_string", "TestType")
    p = any_property_factory()
    assert p.get_base_type_string(quoted=quoted) is expected


@pytest.mark.parametrize(
    "quoted,expected",
    [
        (False, "str"),
        (True, "str"),
    ],
)
def test_get_base_json_type_string(quoted, expected, any_property_factory, mocker):
    from openapi_python_client.parser.properties import AnyProperty

    mocker.patch.object(AnyProperty, "_json_type_string", "str")
    p = any_property_factory()
    assert p.get_base_json_type_string(quoted=quoted) is expected
