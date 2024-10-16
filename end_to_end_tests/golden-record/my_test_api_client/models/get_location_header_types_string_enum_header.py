from enum import Enum
from typing import Literal


class GetLocationHeaderTypesStringEnumHeader(str, Enum):
    ONE = "one"
    THREE = "three"
    TWO = "two"

    def __str__(self) -> str:
        return str(self.value)


GetLocationHeaderTypesStringEnumHeaderLiteral = Literal[
    "one",
    "three",
    "two",
]
