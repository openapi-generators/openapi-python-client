import pytest


class TestProperty:
    def test_is_base_type(self, property_factory):
        assert property_factory().is_base_type is True

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
    def test_get_type_string(self, property_factory, mocker, required, no_optional, json, expected, quoted):
        from openapi_python_client.parser.properties import Property

        mocker.patch.object(Property, "_type_string", "TestType")
        mocker.patch.object(Property, "_json_type_string", "str")
        p = property_factory(required=required)
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
    def test_to_string(self, mocker, default, required, expected, property_factory):
        name = "test"
        mocker.patch("openapi_python_client.parser.properties.Property._type_string", "TestType")
        p = property_factory(name=name, required=required, default=default)

        assert p.to_string() == expected

    def test_get_imports(self, property_factory):
        p = property_factory()
        assert p.get_imports(prefix="") == set()

        p = property_factory(name="test", required=False, default=None)
        assert p.get_imports(prefix="") == {"from types import UNSET, Unset", "from typing import Union"}

    @pytest.mark.parametrize(
        "quoted,expected",
        [
            (False, "TestType"),
            (True, "TestType"),
        ],
    )
    def test_get_base_type_string(self, quoted, expected, property_factory, mocker):
        from openapi_python_client.parser.properties import Property

        mocker.patch.object(Property, "_type_string", "TestType")
        p = property_factory()
        assert p.get_base_type_string(quoted=quoted) is expected

    @pytest.mark.parametrize(
        "quoted,expected",
        [
            (False, "str"),
            (True, "str"),
        ],
    )
    def test_get_base_json_type_string(self, quoted, expected, property_factory, mocker):
        from openapi_python_client.parser.properties import Property

        mocker.patch.object(Property, "_json_type_string", "str")
        p = property_factory()
        assert p.get_base_json_type_string(quoted=quoted) is expected
