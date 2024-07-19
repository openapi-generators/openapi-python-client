from enum import Enum
from typing import Literal


class DifferentEnum(str, Enum):
    DIFFERENT = "DIFFERENT"
    OTHER = "OTHER"

    def __str__(self) -> str:
        return str(self.value)


DifferentEnumLiteral = Literal[
    "DIFFERENT",
    "OTHER",
]
