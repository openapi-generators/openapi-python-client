import re

import stringcase


def snake_case(value: str) -> str:
    value = re.sub(r"([A-Z]{2,})([A-Z][a-z]|[ -_]|$)", lambda m: m.group(1).title() + m.group(2), value.strip())
    value = re.sub(r"(^|[ _-])([A-Z])", lambda m: m.group(1) + m.group(2).lower(), value)
    return stringcase.snakecase(value)


def pascal_case(value: str) -> str:
    return stringcase.pascalcase(value)


def spinal_case(value: str) -> str:
    return stringcase.spinalcase(value)
