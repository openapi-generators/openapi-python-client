from enum import IntEnum
from typing import Literal


class AnIntEnum(IntEnum):
    VALUE_NEGATIVE_1 = -1
    VALUE_1 = 1
    VALUE_2 = 2

    def __str__(self) -> str:
        return str(self.value)


AnIntEnumLiteral = Literal[
    -1,
    1,
    2,
]
