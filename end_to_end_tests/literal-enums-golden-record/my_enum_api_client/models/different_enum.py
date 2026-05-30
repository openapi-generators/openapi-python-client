from typing import Literal

DifferentEnum = Literal["DIFFERENT", "OTHER"]

DIFFERENT_ENUM_VALUES: set[DifferentEnum] = {
    "DIFFERENT",
    "OTHER",
}


def check_different_enum(value: str) -> DifferentEnum:
    if value in DIFFERENT_ENUM_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DIFFERENT_ENUM_VALUES!r}")
