import re

import stringcase


def _sanitize(value: str) -> str:
    return re.sub(r"[^\w _-]+", "", value)


def group_title(value: str) -> str:
    value = re.sub(r"([A-Z]{2,})([A-Z][a-z]|[ -_]|$)", lambda m: m.group(1).title() + m.group(2), value.strip())
    value = re.sub(r"(^|[ _-])([A-Z])", lambda m: m.group(1) + m.group(2).lower(), value)
    return value


def snake_case(value: str) -> str:
    return stringcase.snakecase(group_title(_sanitize(value)))


def pascal_case(value: str) -> str:
    return stringcase.pascalcase(_sanitize(value))


def kebab_case(value: str) -> str:
    return stringcase.spinalcase(group_title(_sanitize(value)))
