from typing import Literal, Set, cast

DifferentEnum = Literal["DIFFERENT", "OTHER"]

DIFFERENT_ENUM_VALUES: Set[DifferentEnum] = {
    "DIFFERENT",
    "OTHER",
}


def check_different_enum(value: str) -> DifferentEnum:
    if value in DIFFERENT_ENUM_VALUES:
        return cast(DifferentEnum, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DIFFERENT_ENUM_VALUES!r}")
