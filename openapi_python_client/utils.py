import re
from keyword import iskeyword

import stringcase


def sanitize(value: str) -> str:
    return re.sub(r"[^\w _\-]+", "", value)


def fix_keywords(value: str) -> str:
    if iskeyword(value):
        return f"{value}_"
    return value


def group_title(value: str) -> str:
    value = re.sub(r"([A-Z]{2,})([A-Z][a-z]|[ \-_]|$)", lambda m: m.group(1).title() + m.group(2), value.strip())
    value = re.sub(r"(^|[ _-])([A-Z])", lambda m: m.group(1) + m.group(2).lower(), value)
    return value


def snake_case(value: str) -> str:
    return fix_keywords(stringcase.snakecase(group_title(sanitize(value))))


def pascal_case(value: str) -> str:
    return fix_keywords(stringcase.pascalcase(sanitize(value)))


def kebab_case(value: str) -> str:
    return fix_keywords(stringcase.spinalcase(group_title(sanitize(value))))


def remove_string_escapes(value: str) -> str:
    return value.replace('"', r"\"")


def to_valid_python_identifier(value: str) -> str:
    """
    Given a string, attempt to coerce it into a valid Python identifier.

    If valid, return it unmodified.

    If invalid, prepend a fixed prefix. This resolves some problems caused by the string's leading
    character.

    If that prefix does not make it a valid identifier - there are unsupported non-leading
    characters - raise a ValueError.

    See:
        https://docs.python.org/3/reference/lexical_analysis.html#identifiers
    """
    if value.isidentifier():
        return value

    new_value = f"field_{value}"

    if new_value.isidentifier():
        return new_value

    raise ValueError(f"Cannot convert {value} to a valid python identifier")
