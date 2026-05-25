from typing import Literal

GetUserListStringEnumHeader = Literal["one", "three", "two"]

GET_USER_LIST_STRING_ENUM_HEADER_VALUES: set[GetUserListStringEnumHeader] = {
    "one",
    "three",
    "two",
}


def check_get_user_list_string_enum_header(value: str) -> GetUserListStringEnumHeader:
    if value in GET_USER_LIST_STRING_ENUM_HEADER_VALUES:
        return value
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_USER_LIST_STRING_ENUM_HEADER_VALUES!r}")
