from enum import Enum


class GetLocationHeaderTypesStringEnumHeader(str, Enum):
    ONE = "one"
    THREE = "three"
    TWO = "two"

    def __str__(self) -> str:
        return str(self.value)
