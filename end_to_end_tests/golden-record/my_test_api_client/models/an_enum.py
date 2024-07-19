from enum import Enum
from typing import Literal


class AnEnum(str, Enum):
    FIRST_VALUE = "FIRST_VALUE"
    SECOND_VALUE = "SECOND_VALUE"

    def __str__(self) -> str:
        return str(self.value)


AnEnumLiteral = Literal[
    "FIRST_VALUE",
    "SECOND_VALUE",
]
