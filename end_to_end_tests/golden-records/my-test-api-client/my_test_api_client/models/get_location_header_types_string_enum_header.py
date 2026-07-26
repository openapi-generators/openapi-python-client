from enum import StrEnum


class GetLocationHeaderTypesStringEnumHeader(StrEnum):
    ONE = "one"
    THREE = "three"
    TWO = "two"

    def __str__(self) -> str:
        return str(self.value)
