from enum import Enum
from typing import Literal


class AnEnumWithNull(str, Enum):
    FIRST_VALUE = "FIRST_VALUE"
    SECOND_VALUE = "SECOND_VALUE"

    def __str__(self) -> str:
        return str(self.value)


AnEnumWithNullLiteral = Literal[
    "FIRST_VALUE",
    "SECOND_VALUE",
]
