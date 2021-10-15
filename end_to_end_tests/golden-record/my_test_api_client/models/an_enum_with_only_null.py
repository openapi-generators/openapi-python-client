from enum import Enum


class AnEnumWithOnlyNull(Enum):
    VALUE_0 = None

    def __str__(self) -> str:
        return str(self.value)
