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


def test__sanitize():
    assert utils.sanitize("something*~with lots_- of weird things}=") == "somethingwith lots_- of weird things"


def test_no_string_escapes():
    assert utils.remove_string_escapes('an "evil" string') == 'an \\"evil\\" string'


def test__fix_keywords():
    assert utils.fix_keywords("None") == "None_"


@pytest.mark.parametrize(
    "reserved_word, expected",
    [
        ("self", "self_"),
        ("int", "int_"),
        ("dict", "dict_"),
        ("not_reserved", "not_reserved"),
        ("type", "type"),
        ("id", "id"),
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
