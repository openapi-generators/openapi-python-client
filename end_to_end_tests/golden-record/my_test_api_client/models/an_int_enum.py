from enum import IntEnum
from typing import Union


class AnIntEnum(IntEnum):
    VALUE_NEGATIVE_1 = -1
    VALUE_1 = 1
    VALUE_2 = 2

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def from_val(cls, value: Union[int, str, "AnIntEnum"]) -> "AnIntEnum":
        if isinstance(value, AnIntEnum):
            return value

        if isinstance(value, str):
            value = value.lower()
            for key in cls.__members__.keys():
                if key.lower() == value:
                    return cls[key]

            # try to convert value to int
            try:
                value = int(value)
            except ValueError:
                pass

        return cls(value)
