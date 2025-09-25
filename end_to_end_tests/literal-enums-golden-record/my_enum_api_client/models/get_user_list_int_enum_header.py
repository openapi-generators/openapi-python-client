from typing import Literal, cast

GetUserListIntEnumHeader = Literal[1, 2, 3]

GET_USER_LIST_INT_ENUM_HEADER_VALUES: set[GetUserListIntEnumHeader] = {
    1,
    2,
    3,
}


def check_get_user_list_int_enum_header(value: int) -> GetUserListIntEnumHeader:
    if value in GET_USER_LIST_INT_ENUM_HEADER_VALUES:
        return cast(GetUserListIntEnumHeader, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_USER_LIST_INT_ENUM_HEADER_VALUES!r}")
