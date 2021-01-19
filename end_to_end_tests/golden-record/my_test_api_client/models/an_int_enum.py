from enum import IntEnum


class AnIntEnum(IntEnum):
    VALUE_NEGATIVE_1 = -1
    VALUE_1 = 1
    VALUE_2 = 2

    def __str__(self) -> str:
        return str(self.value)
