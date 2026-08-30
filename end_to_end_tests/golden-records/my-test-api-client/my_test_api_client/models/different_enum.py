from enum import StrEnum


class DifferentEnum(StrEnum):
    DIFFERENT = "DIFFERENT"
    OTHER = "OTHER"

    def __str__(self) -> str:
        return str(self.value)
