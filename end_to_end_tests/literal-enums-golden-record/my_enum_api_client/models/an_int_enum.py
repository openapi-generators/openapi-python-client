from typing import Literal, cast

AnIntEnum = Literal[-1, 1, 2]

AN_INT_ENUM_VALUES: set[AnIntEnum] = {
    -1,
    1,
    2,
}


def check_an_int_enum(value: int) -> AnIntEnum:
    if value in AN_INT_ENUM_VALUES:
        return cast(AnIntEnum, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AN_INT_ENUM_VALUES!r}")
