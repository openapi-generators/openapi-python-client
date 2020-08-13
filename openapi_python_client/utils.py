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
