import builtins
import re
from keyword import iskeyword
from typing import Any, List

delimiters = " _-"


class PythonIdentifier(str):
    """A string which has been validated / transformed into a valid identifier for Python"""

    def __new__(cls, value: str, prefix: str) -> "PythonIdentifier":
        new_value = fix_reserved_words(fix_keywords(snake_case(sanitize(value))))

        if not new_value.isidentifier():
            new_value = f"{prefix}{new_value}"
        return str.__new__(cls, new_value)

    def __deepcopy__(self, _: Any) -> "PythonIdentifier":
        return self


def sanitize(value: str) -> str:
    """Removes every character that isn't 0-9, A-Z, a-z, or a known delimiter"""
    return re.sub(rf"[^\w{delimiters}]+", "", value)


def split_words(value: str) -> List[str]:
    """Split a string on words and known delimiters"""
    # We can't guess words if there is no capital letter
    if any(c.isupper() for c in value):
        value = " ".join(re.split("([A-Z]?[a-z]+)", value))
    return re.findall(rf"[^{delimiters}]+", value)


def fix_keywords(value: str) -> str:
    if iskeyword(value):
        return f"{value}_"
    return value


RESERVED_WORDS = (set(dir(builtins)) | {"self"}) - {"type", "id"}


def fix_reserved_words(value: str) -> str:
    if value in RESERVED_WORDS:
        return f"{value}_"
    return value


def snake_case(value: str) -> str:
    words = split_words(sanitize(value))
    value = "_".join(words).lower()
    return fix_keywords(value)


def pascal_case(value: str) -> str:
    words = split_words(sanitize(value))
    capitalized_words = (word.capitalize() if not word.isupper() else word for word in words)
    value = "".join(capitalized_words)
    return fix_keywords(value)


def kebab_case(value: str) -> str:
    words = split_words(sanitize(value))
    value = "-".join(words).lower()
    return fix_keywords(value)


def remove_string_escapes(value: str) -> str:
    return value.replace('"', r"\"")
