from enum import IntEnum
from typing import Literal


class AnotherAllOfSubModelTypeEnum(IntEnum):
    VALUE_0 = 0

    def __str__(self) -> str:
        return str(self.value)


AnotherAllOfSubModelTypeEnumLiteral = Literal[0,]
