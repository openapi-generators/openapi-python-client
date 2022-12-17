from enum import Enum


class GetLocationHeaderTypesStringEnumHeader(str, Enum):
    ONE = "one"
    TWO = "two"
    THREE = "three"

    def __str__(self) -> str:
        return str(self.value)
