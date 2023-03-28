import pytest

from openapi_python_client import utils


class TestPythonIdentifier:
    def test_valid_identifier_is_not_changed(self):
        assert utils.PythonIdentifier(value="valid_field", prefix="field") == "valid_field"

    def test_numbers_are_prefixed(self):
        assert utils.PythonIdentifier(value="1", prefix="field") == "field1"

    def test_invalid_symbols_are_stripped(self):
        assert utils.PythonIdentifier(value="$abc", prefix="prefix") == "abc"

    def test_keywords_are_postfixed(self):
        assert utils.PythonIdentifier(value="for", prefix="prefix") == "for_"

    def test_empty_is_prefixed(self):
        assert utils.PythonIdentifier(value="", prefix="something") == "something"


class TestClassName:
    def test_valid_is_not_changed(self):
        assert utils.ClassName(value="ValidClass", prefix="field") == "ValidClass"

    def test_numbers_are_prefixed(self):
        assert utils.ClassName(value="1", prefix="field") == "Field1"

    def test_invalid_symbols_are_stripped(self):
        assert utils.ClassName(value="$abc", prefix="prefix") == "Abc"

    def test_keywords_are_postfixed(self):
        assert utils.ClassName(value="none", prefix="prefix") == "None_"

    def test_empty_is_prefixed(self):
        assert utils.ClassName(value="", prefix="something") == "Something"


@pytest.mark.parametrize(
    "before, after",
    [
        ("connectionID", ["connection", "ID"]),
        ("connection_id", ["connection", "id"]),
        ("connection-id", ["connection", "id"]),
        ("Response200", ["Response", "200"]),
        ("Response200Okay", ["Response", "200", "Okay"]),
        ("S3Config", ["S3", "Config"]),
        ("s3config", ["s3config"]),
        ("fully.qualified.Name", ["fully", "qualified", "Name"]),
    ],
)
def test_split_words(before, after):
    assert utils.split_words(before) == after


def test_snake_case_uppercase_str():
    assert utils.snake_case("HTTP") == "http"
    assert utils.snake_case("HTTP RESPONSE") == "http_response"


def test_snake_case_from_pascal_with_acronyms():
    assert utils.snake_case("HTTPResponse") == "http_response"
    assert utils.snake_case("APIClientHTTPResponse") == "api_client_http_response"
    assert utils.snake_case("OAuthClientHTTPResponse") == "o_auth_client_http_response"
    assert utils.snake_case("S3Config") == "s3_config"


def test_snake_case_from_pascal_with_numbers():
    assert utils.snake_case("Response200") == "response_200"
    assert utils.snake_case("Response200WithContent") == "response_200_with_content"


def test_snake_case_from_pascal():
    assert utils.snake_case("HttpResponsePascalCase") == "http_response_pascal_case"


def test_snake_case_from_camel():
    assert utils.snake_case("httpResponseLowerCamel") == "http_response_lower_camel"
    assert utils.snake_case("connectionID") == "connection_id"


def test_kebab_case():
    assert utils.kebab_case("keep_alive") == "keep-alive"


def test_sanitize():
    assert utils.sanitize("some.thing*~with lots_- of weird things}=") == "some.thingwith lots_- of weird things"


def test_no_string_escapes():
    assert utils.remove_string_escapes('an "evil" string') == 'an \\"evil\\" string'


@pytest.mark.parametrize(
    "reserved_word, expected",
    [
        ("self", "self_"),
        ("int", "int_"),
        ("dict", "dict_"),
        ("not_reserved", "not_reserved"),
        ("type", "type"),
        ("id", "id"),
        ("None", "None_"),
    ],
)
def test__fix_reserved_words(reserved_word: str, expected: str):
    assert utils.fix_reserved_words(reserved_word) == expected


@pytest.mark.parametrize(
    "before, after",
    [
        ("PascalCase", "PascalCase"),
        ("snake_case", "SnakeCase"),
        ("TLAClass", "TLAClass"),
        ("Title Case", "TitleCase"),
        ("s3_config", "S3Config"),
        ("__LeadingUnderscore", "LeadingUnderscore"),
    ],
)
def test_pascalcase(before, after):
    assert utils.pascal_case(before) == after


@pytest.mark.parametrize(
    "content_type, expected",
    [
        pytest.param("application/json", "application/json"),
        pytest.param("application/vnd.api+json", "application/vnd.api+json"),
        pytest.param("application/json;charset=utf-8", "application/json"),
        pytest.param("application/vnd.api+json;charset=utf-8", "application/vnd.api+json"),
    ],
)
def test_get_content_type(content_type: str, expected: str) -> None:
    assert utils.get_content_type(content_type) == expected
