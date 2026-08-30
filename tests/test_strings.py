import ast
import copy
import textwrap
import warnings

import pytest

from openapi_python_client import strings
from openapi_python_client.schema.untrusted_string import UntrustedString


class TestPythonIdentifier:
    def test_valid_identifier_is_not_changed(self):
        assert strings.PythonIdentifier(value="valid_field", prefix="field") == "valid_field"

    def test_numbers_are_prefixed(self):
        assert strings.PythonIdentifier(value="1", prefix="field") == "field1"

    def test_invalid_symbols_are_stripped(self):
        assert strings.PythonIdentifier(value="$abc", prefix="prefix") == "abc"

    def test_keywords_are_postfixed(self):
        assert strings.PythonIdentifier(value="for", prefix="prefix") == "for_"

    def test_empty_is_prefixed(self):
        assert strings.PythonIdentifier(value="", prefix="something") == "something"

    def test_skip_snake_case_preserves_case(self):
        assert strings.PythonIdentifier(value="fooBar", prefix="field", skip_snake_case=True) == "fooBar"

    def test_skip_snake_case_strips_delimiters(self):
        assert strings.PythonIdentifier(value="foo-bar", prefix="field", skip_snake_case=True) == "foobar"
        assert strings.PythonIdentifier(value="foo bar", prefix="field", skip_snake_case=True) == "foobar"
        assert strings.PythonIdentifier(value="foo.bar", prefix="field", skip_snake_case=True) == "foobar"

    def test_skip_snake_case_keeps_underscores(self):
        assert strings.PythonIdentifier(value="foo_bar", prefix="field", skip_snake_case=True) == "foo_bar"

    def test_skip_snake_case_result_is_always_valid_identifier(self):
        result = strings.PythonIdentifier(value="foo-bar", prefix="field", skip_snake_case=True)
        assert result.isidentifier()
        assert strings.PythonIdentifier(value="1-2", prefix="field", skip_snake_case=True).isidentifier()
        assert strings.PythonIdentifier(value="---", prefix="field", skip_snake_case=True).isidentifier()

    def test_non_identifier_unicode_is_stripped(self):
        # U+00BC VULGAR FRACTION ONE QUARTER matches \w but is not valid in identifiers
        assert strings.PythonIdentifier(value="¼", prefix="field") == "field"
        assert strings.PythonIdentifier(value="¼", prefix="field").isidentifier()


class TestClassName:
    def test_valid_is_not_changed(self):
        assert strings.ClassName(value=UntrustedString("ValidClass"), prefix="field") == "ValidClass"

    def test_numbers_are_prefixed(self):
        assert strings.ClassName(value=UntrustedString("1"), prefix="field") == "Field1"

    def test_invalid_symbols_are_stripped(self):
        assert strings.ClassName(value=UntrustedString("$abc"), prefix="prefix") == "Abc"

    def test_keywords_are_postfixed(self):
        assert strings.ClassName(value=UntrustedString("none"), prefix="prefix") == "None_"

    def test_empty_is_prefixed(self):
        assert strings.ClassName(value=UntrustedString(""), prefix="something") == "Something"

    def test_deepcopy_returns_self(self):
        name = strings.ClassName(value=UntrustedString("ValidClass"), prefix="field")
        assert copy.deepcopy(name) is name


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
    assert strings.split_words(before) == after


def test_snake_case_uppercase_str():
    assert strings.snake_case("HTTP") == "http"
    assert strings.snake_case("HTTP RESPONSE") == "http_response"


def test_snake_case_from_pascal_with_acronyms():
    assert strings.snake_case("HTTPResponse") == "http_response"
    assert strings.snake_case("APIClientHTTPResponse") == "api_client_http_response"
    assert strings.snake_case("OAuthClientHTTPResponse") == "o_auth_client_http_response"
    assert strings.snake_case("S3Config") == "s3_config"


def test_snake_case_from_pascal_with_numbers():
    assert strings.snake_case("Response200") == "response_200"
    assert strings.snake_case("Response200WithContent") == "response_200_with_content"


def test_snake_case_from_pascal():
    assert strings.snake_case("HttpResponsePascalCase") == "http_response_pascal_case"


def test_snake_case_from_camel():
    assert strings.snake_case("httpResponseLowerCamel") == "http_response_lower_camel"
    assert strings.snake_case("connectionID") == "connection_id"


def test_snake_case_untrusted_string():
    assert strings.snake_case(UntrustedString("httpResponse")) == "http_response"


def test_kebab_case():
    assert strings.kebab_case("keep_alive") == "keep-alive"


def test_sanitize():
    assert strings.sanitize("some.thing*~with lots_- of weird things}=") == "some.thingwith lots_- of weird things"


def test_sanitize_strips_non_identifier_unicode():
    # ¼ matches \w but cannot appear in a Python identifier; digits must be kept for splitting
    assert strings.sanitize("¼") == ""
    assert strings.sanitize("S3Config") == "S3Config"


def test_split_words_on_backslash():
    # Backslash is a delimiter; it must actually split, not leak into the word
    assert strings.split_words("one\\two") == ["one", "two"]
    assert strings.snake_case("one\\two") == "one_two"


@pytest.mark.parametrize(
    "value, expected",
    [
        ('an "evil" string', r"an \"evil\" string"),
        (r"an \"evil string", r"an \\\"evil string"),
    ],
)
def test_no_string_escapes(value: str, expected: str):
    assert strings.remove_string_escapes(value) == expected


@pytest.mark.parametrize(
    "reserved_word, expected",
    [
        ("self", "self_"),
        ("int", "int_"),
        ("dict", "dict_"),
        ("not_reserved", "not_reserved"),
        ("type", "type_"),
        ("id", "id"),
        ("None", "None_"),
    ],
)
def test__fix_reserved_words(reserved_word: str, expected: str):
    assert strings.fix_reserved_words(reserved_word) == expected


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
    assert strings.pascal_case(before) == after


@pytest.mark.parametrize(
    "content_type, expected",
    [
        pytest.param("application/json", "application/json"),
        pytest.param("application/vnd.api+json", "application/vnd.api+json"),
        pytest.param("application/json;charset=utf-8", "application/json"),
        pytest.param("application/vnd.api+json;charset=utf-8", "application/vnd.api+json"),
    ],
)
def test_get_content_type(content_type: str, expected: str, config) -> None:
    assert strings.get_content_type(content_type, config) == expected


@pytest.mark.parametrize(
    "untrusted, expected",
    [
        ("innocuous", "innocuous"),
        ('can contain "quotes"', 'can contain "quotes"'),
        ("backslash\\ should be escaped", "backslash\\\\ should be escaped"),
        ('triple quotes """ are an issue', 'triple quotes \\"\\"\\" are an issue'),
        # Control characters which are illegal in Python source must be stripped
        ("null\x00byte", "nullbyte"),
        ("bell\x07rings", "bellrings"),
        ("newlines\nand\ttabs\r\nstay", "newlines\nand\ttabs\r\nstay"),
    ],
)
def test_safe_for_docstring(untrusted: str, expected: str) -> None:
    assert strings.safe_for_docstring(UntrustedString(untrusted)) == expected


def test_safe_for_docstring_non_string() -> None:
    """Non-string values (e.g. dict examples) are stringified instead of crashing"""
    assert strings.safe_for_docstring({"nested": 'has "quotes"'}) == "{'nested': 'has \"quotes\"'}"


@pytest.mark.parametrize(
    "untrusted, expected",
    [
        ("innocuous", "innocuous"),
        ('quotes "break out" of literals', 'quotes \\"break out\\" of literals'),
        ("backslash\\ escapes", "backslash\\\\ escapes"),
        ("newlines\nand\ttabs", "newlinesand\\ttabs"),
        ("backspace\bform-feed\f", "backspace\\bform-feed\\f"),
        ("single 'quotes' are fine", "single 'quotes' are fine"),
        ("astral character \U00010000", "astral character \U00010000"),
        ("\x7f\N{NEXT LINE}\N{LINE SEPARATOR}\N{PARAGRAPH SEPARATOR}", ""),
        ("bidirectional\u202etext", "bidirectionaltext"),
    ],
)
def test_in_double_quote_literal(untrusted: str, expected: str) -> None:
    assert strings.in_double_quote_literal(UntrustedString(untrusted)) == expected


@pytest.mark.parametrize(
    "untrusted, expected",
    [
        ("innocuous", "innocuous"),
        ('quotes "break out"', 'quotes \\"break out\\"'),
        ("{braces} inject code", "{{braces}} inject code"),
        ("{x!r:>10}", "{{x!r:>10}}"),
        ("backslash\\", "backslash\\\\"),
    ],
)
def test_in_f_string_literal(untrusted: str, expected: str) -> None:
    assert strings.in_f_string_literal(UntrustedString(untrusted)) == expected


class TestPythonCode:
    def test_get_code_returns_raw_source(self) -> None:
        assert strings.PythonCode("'some' + code").as_unembedded_code() == "'some' + code"

    def test_repr_does_not_contain_code(self) -> None:
        """The repr is what a template that forgets to unwrap renders: it must never contain the code"""
        code = strings.PythonCode('""" + print("uh oh")')
        assert "print" not in repr(code)
        assert "PythonCode object at 0x" in repr(code)

    def test_no_str(self) -> None:
        """PythonCode must not be implicitly convertible to str, so str() falls back to the safe repr"""
        assert "__str__" not in vars(strings.PythonCode)
        code = strings.PythonCode("1 + 1")
        assert str(code) == repr(code)
        assert "1 + 1" not in str(code)


def test_in_double_quote_literal_accepts_python_code() -> None:
    assert strings.in_double_quote_literal(strings.PythonCode('"quoted"')) == '\\"quoted\\"'


def test_safe_for_docstring_accepts_python_code() -> None:
    assert strings.safe_for_docstring(strings.PythonCode('a"""b')) == 'a\\"\\"\\"b'


def _wordwrap_like_templates(text: str, width: int) -> str:
    """Replicates the `wordwrap` filter as used in templates (per-paragraph textwrap)"""
    return "\n".join(
        "\n".join(
            textwrap.wrap(
                line,
                width=width,
                expand_tabs=False,
                replace_whitespace=False,
                break_long_words=True,
                break_on_hyphens=True,
            )
        )
        for line in text.splitlines()
    )


# Widths passed to the wordwrap filter in templates
@pytest.mark.parametrize("width", [90, 100, 101, 112, 116])
def test_safe_for_docstring_output_survives_wordwrap(width: int) -> None:
    """wordwrap hard-splits over-long words; escaped content must stay valid Python wherever it lands"""
    nasty = (
        'has """ triple \\ quotes and \U001060ef astral chars and \x00nulls ' * 5
        # One long unbroken word: \U and \N are hard SyntaxErrors if a split leaves them dangling
        + r"C:\Users\New\Documents\foo" * 8
        + " "
        + '"' * 200
    )
    escaped = strings.safe_for_docstring(nasty)
    wrapped = _wordwrap_like_templates(escaped, width)
    with warnings.catch_warnings():
        warnings.simplefilter("error")  # invalid escape sequences would warn (SyntaxError in future Python)
        parsed = ast.parse(f'"""\n{wrapped}\n"""')
    docstring = parsed.body[0].value.value
    assert isinstance(docstring, str)  # nothing broke out of the docstring


def test_safe_for_docstring_chunks_long_words_at_escape_safe_points() -> None:
    """Inserted line breaks must not interrupt an escape sequence or change the content"""
    word = r"C:\Users\New\Documents\foo" * 8
    escaped = strings.safe_for_docstring(word)
    lines = escaped.split("\n")
    assert len(lines) > 1
    assert all(len(line) <= strings._MAX_ESCAPED_WORD_LENGTH for line in lines)
    for line in lines:
        trailing_backslashes = len(line) - len(line.rstrip("\\"))
        assert trailing_backslashes % 2 == 0
    # Only newlines were inserted; the escaped content is otherwise untouched
    assert escaped.replace("\n", "") == word.replace("\\", "\\\\")


def test_safe_for_docstring_does_not_chunk_words_without_backslashes() -> None:
    """Words with no escape sequences (e.g. URLs) can be hard-split anywhere, so leave them alone"""
    word = "https://example.com/" + "a" * 500
    assert strings.safe_for_docstring(word) == word
