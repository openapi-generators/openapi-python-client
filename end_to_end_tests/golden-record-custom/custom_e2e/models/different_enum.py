from enum import Enum


class DifferentEnum(str, Enum):
    DIFFERENT = "DIFFERENT"
    OTHER = "OTHER"

    def __str__(self) -> str:
        return str(self.value)
