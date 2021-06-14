from openapi_python_client.parser.properties.property import to_valid_python_identifier


class TestToValidPythonIdentifier:
    def test_valid_identifier_is_not_changed(self):
        assert to_valid_python_identifier("valid_field", prefix="field") == "valid_field"

    def test_numbers_are_prefixed(self):
        assert to_valid_python_identifier("1", prefix="field") == "field1"

    def test_invalid_symbols_are_stripped(self):
        assert to_valid_python_identifier("$abc", "prefix") == "abc"

    def test_keywords_are_postfixed(self):
        assert to_valid_python_identifier("for", "prefix") == "for_"

    def test_empty_is_prefixed(self):
        assert to_valid_python_identifier("", "something") == "something"
