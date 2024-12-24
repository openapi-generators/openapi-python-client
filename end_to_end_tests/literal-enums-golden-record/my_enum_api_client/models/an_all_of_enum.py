from typing import Literal, cast

AnAllOfEnum = Literal["a_default", "bar", "foo", "overridden_default"]

AN_ALL_OF_ENUM_VALUES: set[AnAllOfEnum] = {
    "a_default",
    "bar",
    "foo",
    "overridden_default",
}


def check_an_all_of_enum(value: str) -> AnAllOfEnum:
    if value in AN_ALL_OF_ENUM_VALUES:
        return cast(AnAllOfEnum, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AN_ALL_OF_ENUM_VALUES!r}")
