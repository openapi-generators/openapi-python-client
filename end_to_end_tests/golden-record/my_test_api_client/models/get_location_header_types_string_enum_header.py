from enum import Enum
from typing import Union


class GetLocationHeaderTypesStringEnumHeader(str, Enum):
    ONE = "one"
    THREE = "three"
    TWO = "two"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def from_val(
        cls, value: Union[str, "GetLocationHeaderTypesStringEnumHeader"]
    ) -> "GetLocationHeaderTypesStringEnumHeader":
        if isinstance(value, GetLocationHeaderTypesStringEnumHeader):
            return value

        value = value.lower()

        for enum in cls:
            if enum.value.lower() == value:
                return enum

        return GetLocationHeaderTypesStringEnumHeader(value)
