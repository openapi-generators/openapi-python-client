import attr
import pytest

from openapi_python_client.parser.properties.property import to_valid_python_identifier


class TestToValidPythonIdentifier:
    def test_valid_identifier_is_not_changed(self):
        assert to_valid_python_identifier(value="valid_field", prefix="field") == "valid_field"

    def test_numbers_are_prefixed(self):
        assert to_valid_python_identifier(value="1", prefix="field") == "field1"

    def test_invalid_symbols_are_stripped(self):
        assert to_valid_python_identifier(value="$abc", prefix="prefix") == "abc"

    def test_keywords_are_postfixed(self):
        assert to_valid_python_identifier(value="for", prefix="prefix") == "for_"

    def test_empty_is_prefixed(self):
        assert to_valid_python_identifier(value="", prefix="something") == "something"


class TestProperty:
    @pytest.mark.parametrize(
        "nullable,required,no_optional,json,expected",
        [
            (False, False, False, False, "Union[Unset, TestType]"),
            (False, False, True, False, "TestType"),
            (False, True, False, False, "TestType"),
            (False, True, True, False, "TestType"),
            (True, False, False, False, "Union[Unset, None, TestType]"),
            (True, False, True, False, "TestType"),
            (True, True, False, False, "Optional[TestType]"),
            (True, True, True, False, "TestType"),
            (False, False, False, True, "Union[Unset, str]"),
            (False, False, True, True, "str"),
            (False, True, False, True, "str"),
            (False, True, True, True, "str"),
            (True, False, False, True, "Union[Unset, None, str]"),
            (True, False, True, True, "str"),
            (True, True, False, True, "Optional[str]"),
            (True, True, True, True, "str"),
        ],
    )
    def test_get_type_string(self, property_factory, mocker, nullable, required, no_optional, json, expected):
        from openapi_python_client.parser.properties import Property

        mocker.patch.object(Property, "_type_string", "TestType")
        mocker.patch.object(Property, "_json_type_string", "str")
        p = property_factory(required=required, nullable=nullable)
        assert p.get_type_string(no_optional=no_optional, json=json) == expected

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
        from openapi_python_client.parser.properties import Property

        p = property_factory()
        assert p.get_imports(prefix="") == set()

        p = property_factory(name="test", required=False, default=None, nullable=False)
        assert p.get_imports(prefix="") == {"from types import UNSET, Unset", "from typing import Union"}

        p = property_factory(name="test", required=False, default=None, nullable=True)
        assert p.get_imports(prefix="") == {
            "from types import UNSET, Unset",
            "from typing import Optional",
            "from typing import Union",
        }
