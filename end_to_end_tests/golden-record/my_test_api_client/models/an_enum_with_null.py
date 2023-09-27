from enum import Enum
from typing import Union


class AnEnumWithNull(str, Enum):
    FIRST_VALUE = "FIRST_VALUE"
    SECOND_VALUE = "SECOND_VALUE"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def from_val(cls, value: Union[str, "AnEnumWithNull"]) -> "AnEnumWithNull":
        if isinstance(value, AnEnumWithNull):
            return value

        value = value.lower()

        for enum in cls:
            if enum.value.lower() == value:
                return enum

        return AnEnumWithNull(value)
