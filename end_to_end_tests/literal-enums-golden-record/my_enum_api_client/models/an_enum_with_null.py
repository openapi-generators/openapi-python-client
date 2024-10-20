from typing import Literal, cast

AnEnumWithNull = Literal["FIRST_VALUE", "SECOND_VALUE"]

AN_ENUM_WITH_NULL_VALUES: set[AnEnumWithNull] = {
    "FIRST_VALUE",
    "SECOND_VALUE",
}


def check_an_enum_with_null(value: str) -> AnEnumWithNull:
    if value in AN_ENUM_WITH_NULL_VALUES:
        return cast(AnEnumWithNull, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AN_ENUM_WITH_NULL_VALUES!r}")
