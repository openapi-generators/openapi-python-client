import builtins
import re
from keyword import iskeyword
from typing import Any, List

DELIMITERS = r"\. _-"


class PythonIdentifier(str):
    """A snake_case string which has been validated / transformed into a valid identifier for Python"""

    def __new__(cls, value: str, prefix: str) -> "PythonIdentifier":
        new_value = fix_reserved_words(snake_case(sanitize(value)))

        if not new_value.isidentifier():
            new_value = f"{prefix}{new_value}"
        return str.__new__(cls, new_value)

    def __deepcopy__(self, _: Any) -> "PythonIdentifier":
        return self


class ClassName(str):
    """A PascalCase string which has been validated / transformed into a valid class name for Python"""

    def __new__(cls, value: str, prefix: str) -> "ClassName":
        new_value = fix_reserved_words(pascal_case(sanitize(value)))

        if not new_value.isidentifier():
            value = f"{prefix}{new_value}"
            new_value = fix_reserved_words(pascal_case(sanitize(value)))
        return str.__new__(cls, new_value)

    def __deepcopy__(self, _: Any) -> "ClassName":
        return self


def sanitize(value: str) -> str:
    """Removes every character that isn't 0-9, A-Z, a-z, or a known delimiter"""
    return re.sub(rf"[^\w{DELIMITERS}]+", "", value)


def split_words(value: str) -> List[str]:
    """Split a string on words and known delimiters"""
    # We can't guess words if there is no capital letter
    if any(c.isupper() for c in value):
        value = " ".join(re.split("([A-Z]?[a-z]+)", value))
    return re.findall(rf"[^{DELIMITERS}]+", value)


RESERVED_WORDS = (set(dir(builtins)) | {"self", "true", "false", "datetime"}) - {"type", "id"}


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


def snake_case(value: str) -> str:
    """Converts to snake_case"""
    words = split_words(sanitize(value))
    return "_".join(words).lower()


def pascal_case(value: str) -> str:
    """Converts to PascalCase"""
    words = split_words(sanitize(value))
    capitalized_words = (word.capitalize() if not word.isupper() else word for word in words)
    return "".join(capitalized_words)


def kebab_case(value: str) -> str:
    """Converts to kebab-case"""
    words = split_words(sanitize(value))
    return "-".join(words).lower()


def remove_string_escapes(value: str) -> str:
    """Used when parsing string-literal defaults to prevent escaping the string to write arbitrary Python

    **REMOVING OR CHANGING THE USAGE OF THIS FUNCTION HAS SECURITY IMPLICATIONS**

    See Also:
        - https://github.com/openapi-generators/openapi-python-client/security/advisories/GHSA-9x4c-63pf-525f
    """
    return value.replace('"', r"\"")
