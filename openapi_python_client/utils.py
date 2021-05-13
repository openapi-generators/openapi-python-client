import builtins
import re
from keyword import iskeyword
from typing import List

delimiters = " _-"


def sanitize(value: str) -> str:
    """Removes every character that isn't 0-9, A-Z, a-z, or a known delimiter"""
    return re.sub(rf"[^\w{delimiters}]+", "", value)


def split_words(value: str) -> List[str]:
    """Split a string on non-capital letters and known delimiters"""
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


# This can be changed by config.Config.load_config
FIELD_PREFIX = "field_"


def to_valid_python_identifier(value: str) -> str:
    """
    Given a string, attempt to coerce it into a valid Python identifier by stripping out invalid characters and, if
    necessary, prepending a prefix.

    See:
        https://docs.python.org/3/reference/lexical_analysis.html#identifiers
    """
    new_value = fix_reserved_words(fix_keywords(sanitize(value)))

    if new_value.isidentifier():
        return new_value

    return f"{FIELD_PREFIX}{new_value}"
