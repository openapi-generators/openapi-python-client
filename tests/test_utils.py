from openapi_python_client import utils


def test_snake_case_uppercase_str():
    assert utils.snake_case("HTTP") == "http"
    assert utils.snake_case("HTTP RESPONSE") == "http_response"


def test_snake_case_from_pascal_with_acronyms():
    assert utils.snake_case("HTTPResponse") == "http_response"
    assert utils.snake_case("APIClientHTTPResponse") == "api_client_http_response"
    assert utils.snake_case("OAuthClientHTTPResponse") == "o_auth_client_http_response"


def test_snake_case_from_pascal():
    assert utils.snake_case("HttpResponsePascalCase") == "http_response_pascal_case"


def test_snake_case_from_camel():
    assert utils.snake_case("httpResponseLowerCamel") == "http_response_lower_camel"


def test_kebab_case():
    assert utils.kebab_case("keep_alive") == "keep-alive"


def test__sanitize():
    assert utils.sanitize("something*~with lots_- of weird things}=") == "somethingwith lots_- of weird things"


def test_no_string_escapes():
    assert utils.remove_string_escapes('an "evil" string') == 'an \\"evil\\" string'


def test__fix_keywords():
    assert utils.fix_keywords("None") == "None_"


def test_to_valid_python_identifier():
    assert utils.to_valid_python_identifier("valid") == "valid"
    assert utils.to_valid_python_identifier("1") == "field_1"
    assert utils.to_valid_python_identifier("$") == "field_"
    assert utils.to_valid_python_identifier("for") == "for_"
