from typing import Literal, cast

AnEnum = Literal["FIRST_VALUE", "SECOND_VALUE"]

AN_ENUM_VALUES: set[AnEnum] = {
    "FIRST_VALUE",
    "SECOND_VALUE",
}


def check_an_enum(value: str) -> AnEnum:
    if value in AN_ENUM_VALUES:
        return cast(AnEnum, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AN_ENUM_VALUES!r}")
