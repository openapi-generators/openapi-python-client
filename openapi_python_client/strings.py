from __future__ import annotations

import builtins
import json
import re
import unicodedata
from dataclasses import dataclass
from email.message import Message
from keyword import iskeyword
from typing import Any

from .config import Config
from .schema.untrusted_string import UntrustedString

DELIMITERS = r"\. _-"


@dataclass(frozen=True, repr=False, slots=True)
class PythonCode:
    """
    A snippet of Python source code generated from `UnstrustedString`s.

    It's safe to treat as code, but _may not_ be safe to place in docstrings, f-strings, etc.
    """

    _code: str

    def as_unembedded_code(self) -> str:
        """
        Return the raw source code with no transformations.

        DO NOT use this inside a string context (docstrings, string literals, f-string literal text).
        Pass this through the appropriate escaping function first (e.g. `safe_for_docstring`).
        """
        return self._code


class PythonIdentifier(str):
    """A snake_case string which has been validated / transformed into a valid identifier for Python"""

    def __new__(cls, value: UntrustedString | str, prefix: str, skip_snake_case: bool = False) -> PythonIdentifier:
        if isinstance(value, UntrustedString):
            value = value.get_untrusted_value()
        safe_value = sanitize(value)
        leading_underscore = safe_value.startswith("_")
        if skip_snake_case:
            # Keep the name as close to the original as possible (to disambiguate conflicts);
            # only strip the delimiters sanitize() preserved, as they aren't valid in identifiers
            safe_value = re.sub(r"[^\w]+", "", safe_value)
        else:
            safe_value = snake_case(safe_value)
        safe_value = fix_reserved_words(safe_value)

        if not safe_value.isidentifier() or leading_underscore:
            safe_value = f"{prefix}{safe_value}"
        return str.__new__(cls, safe_value)

    def __deepcopy__(self, _: Any) -> PythonIdentifier:
        return self


class ClassName(str):
    """A PascalCase string which has been validated / transformed into a valid class name for Python"""

    def __new__(cls, value: UntrustedString | str, prefix: str) -> ClassName:
        safe_value = fix_reserved_words(pascal_case(value))

        if not safe_value.isidentifier():
            safe_value = f"{prefix}{safe_value}"
            safe_value = fix_reserved_words(pascal_case(safe_value))
        return str.__new__(cls, safe_value)

    def __deepcopy__(self, _: Any) -> ClassName:
        return self


def sanitize(value: str) -> str:
    """Removes every character that isn't 0-9, A-Z, a-z, or a known delimiter"""
    return "".join(c for c in value if c.isidentifier() or c.isdecimal() or c in DELIMITERS)


def split_words(value: str) -> list[str]:
    """Split a string on words and known delimiters"""
    if any(c.isupper() for c in value):
        value = " ".join(re.split("([A-Z]?[a-z]+)", value))
    return re.findall(rf"[^{re.escape(DELIMITERS)}]+", value)


RESERVED_WORDS = (set(dir(builtins)) | {"self", "true", "false", "datetime"}) - {
    "id",
}


def fix_reserved_words(value: str) -> str:
    """
    Using reserved Python words as identifiers in generated code causes problems, so this function renames them.

    Args:
        value: The identifier to-be that should be renamed if it's a reserved word.

    Returns:
        `value` suffixed with `_` if it was a reserved word.
    """
    if value in RESERVED_WORDS or iskeyword(value):
        return f"{value}_"
    return value


def snake_case(value: str | UntrustedString) -> str:
    """Converts to snake_case identifier, stripping all non-alphanumeric characters"""
    if isinstance(value, UntrustedString):
        value = value.get_untrusted_value()
    words = split_words(sanitize(value))
    return "_".join(words).lower()


def pascal_case(value: str | UntrustedString) -> str:
    """Converts to PascalCase identifier, stripping all non-alphanumeric characters"""
    if isinstance(value, UntrustedString):
        value = value.get_untrusted_value()
    words = split_words(sanitize(value))
    capitalized_words = (word.capitalize() if not word.isupper() else word for word in words)
    return "".join(capitalized_words)


def kebab_case(value: str | UntrustedString) -> str:
    """Converts to kebab-case identifier, stripping all non-alphanumeric characters"""
    if isinstance(value, UntrustedString):
        value = value.get_untrusted_value()
    words = split_words(sanitize(value))
    return "-".join(words).lower()


#: Escaped words in docstring content are kept shorter than this so the ``wordwrap`` filter
#: never hard-splits inside an escape sequence (the narrowest wordwrap width in templates is 90).
_MAX_ESCAPED_WORD_LENGTH = 76


def _split_long_word_safely(word: str) -> str:
    """Insert newlines into an over-long escaped word where they can't interrupt an escape sequence.

    wordwrap hard-splits words longer than its width at arbitrary positions. A split between the
    backslashes of ``\\\\`` leaves a lone backslash at the start of the next line, where it forms an
    invalid escape (``\\ `` warns today and will error in a future Python) or even a ``SyntaxError``
    (``\\U`` + non-hex is a truncated escape). Splits right after an even number of backslashes are
    always safe: the prefix ends with complete escapes and the suffix can't start a dangling one.
    """
    chunks: list[str] = []
    start = 0
    while len(word) - start > _MAX_ESCAPED_WORD_LENGTH:
        end = start + _MAX_ESCAPED_WORD_LENGTH
        run = 0
        while end > start and word[end - 1] == "\\":
            end -= 1
            run += 1
        # Keep an even number of trailing backslashes in this chunk. Odd runs only occur right
        # before an escaped quote, so the one left behind always forms a valid `\"`.
        end += run - (run % 2)
        chunks.append(word[start:end])
        start = end
    chunks.append(word[start:])
    return "\n".join(chunks)


def safe_for_docstring(value: Any) -> str:
    """
    Remove any risky escapes from docstring content.

    The output is safe to run through the ``wordwrap`` filter at any width greater than
    ``_MAX_ESCAPED_WORD_LENGTH``: over-long words containing escape sequences are pre-split where
    no escape sequence is interrupted, so wordwrap's hard-splitting can't create invalid escapes.
    """
    if isinstance(value, UntrustedString):
        value = value.get_untrusted_value()
    if isinstance(value, PythonCode):
        value = value.as_unembedded_code()
    if not isinstance(value, str):
        value = str(value)
    # Strip control characters which are illegal in Python source (e.g. null bytes)
    value = "".join(c for c in value if unicodedata.category(c) != "Cc" or c in "\n\r\t")

    value = value.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
    # Words without backslashes can be hard-split anywhere safely, so leave them alone
    return re.sub(
        r"\S+",
        lambda match: _split_long_word_safely(match.group()) if "\\" in match.group() else match.group(),
        value,
    )


def in_double_quote_literal(value: UntrustedString | PythonCode | str) -> str:
    """Escape a string so it can be safely embedded inside a double-quoted string literal.

    The result does NOT include surrounding quotes; the caller is expected to place it inside its own `"..."`
    (e.g. a Python string literal or a TOML string in generated code). JSON encoding is used for the escaping,
    which is valid inside both Python and TOML double-quoted strings.
    """
    if isinstance(value, UntrustedString):
        value = value.get_untrusted_value()
    if isinstance(value, PythonCode):
        value = value.as_unembedded_code()
    value = "".join(
        character
        for character in value
        if (character in "\b\t\f" or not unicodedata.category(character).startswith("C"))
        and unicodedata.category(character) not in {"Zl", "Zp"}
    )
    return json.dumps(value, ensure_ascii=False)[1:-1]


def in_f_string_literal(value: UntrustedString | PythonCode | str) -> str:
    """Escape a string so it can be safely embedded as literal text inside a double-quoted f-string.

    In addition to the double-quoted-string escaping (quotes, backslashes), this escapes `{` and `}` as
    `{{` and `}}` so the value cannot be interpreted as an f-string replacement field or format specifier.
    Without this, an untrusted value could inject arbitrary expressions into the generated f-string.
    """
    return in_double_quote_literal(value).replace("{", "{{").replace("}", "}}")


def remove_string_escapes(value: str) -> str:
    """Used when parsing string-literal defaults to prevent escaping the string to write arbitrary Python

    **REMOVING OR CHANGING THE USAGE OF THIS FUNCTION HAS SECURITY IMPLICATIONS**

    See Also:
        - https://github.com/openapi-generators/openapi-python-client/security/advisories/GHSA-9x4c-63pf-525f
    """
    return value.replace("\\", "\\\\").replace('"', r"\"")


def get_content_type(content_type: str, config: Config) -> str | None:
    """
    Given a string representing a content type with optional parameters, returns the content type only
    """
    content_type = config.content_type_overrides.get(content_type, content_type)
    message = Message()
    message.add_header("Content-Type", content_type)

    parsed_content_type = message.get_content_type()
    if not content_type.startswith(parsed_content_type):
        # Always defaults to `text/plain` if it's not recognized. We want to return an error, not default.
        return None

    return parsed_content_type
