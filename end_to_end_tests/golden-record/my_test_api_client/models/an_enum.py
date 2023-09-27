from enum import Enum
from typing import Union


class AnEnum(str, Enum):
    FIRST_VALUE = "FIRST_VALUE"
    SECOND_VALUE = "SECOND_VALUE"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def from_val(cls, value: Union[str, "AnEnum"]) -> "AnEnum":
        if isinstance(value, AnEnum):
            return value

        value = value.lower()

        for enum in cls:
            if enum.value.lower() == value:
                return enum

        return AnEnum(value)
