from enum import Enum


class AnEnum(str, Enum):
    FIRST_VALUE = "FIRST_VALUE"
    SECOND_VALUE = "SECOND_VALUE"

    def __str__(self) -> str:
        return str(self.value)
