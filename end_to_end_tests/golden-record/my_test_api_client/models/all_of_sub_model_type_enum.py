from enum import IntEnum
from typing import Literal


class AllOfSubModelTypeEnum(IntEnum):
    VALUE_0 = 0
    VALUE_1 = 1

    def __str__(self) -> str:
        return str(self.value)


AllOfSubModelTypeEnumLiteral = Literal[
    0,
    1,
]
