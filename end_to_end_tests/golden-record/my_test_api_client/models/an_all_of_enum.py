from enum import Enum
from typing import Union


class AnAllOfEnum(str, Enum):
    A_DEFAULT = "a_default"
    BAR = "bar"
    FOO = "foo"
    OVERRIDDEN_DEFAULT = "overridden_default"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def from_val(cls, value: Union[str, "AnAllOfEnum"]) -> "AnAllOfEnum":
        if isinstance(value, AnAllOfEnum):
            return value

        value = value.lower()

        for enum in cls:
            if enum.value.lower() == value:
                return enum

        return AnAllOfEnum(value)
