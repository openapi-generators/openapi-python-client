from enum import Enum
from typing import Union


class DifferentEnum(str, Enum):
    DIFFERENT = "DIFFERENT"
    OTHER = "OTHER"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def from_val(cls, value: Union[str, "DifferentEnum"]) -> "DifferentEnum":
        if isinstance(value, DifferentEnum):
            return value

        value = value.lower()

        for enum in cls:
            if enum.value.lower() == value:
                return enum

        return DifferentEnum(value)
