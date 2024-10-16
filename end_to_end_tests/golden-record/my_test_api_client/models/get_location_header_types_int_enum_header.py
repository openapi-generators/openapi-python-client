from enum import IntEnum
from typing import Literal


class GetLocationHeaderTypesIntEnumHeader(IntEnum):
    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3

    def __str__(self) -> str:
        return str(self.value)


GetLocationHeaderTypesIntEnumHeaderLiteral = Literal[
    1,
    2,
    3,
]
