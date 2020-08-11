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


def test_spinal_case():
    assert utils.spinal_case("keep_alive") == "keep-alive"
