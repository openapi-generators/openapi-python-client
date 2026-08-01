from enum import Enum


class GetContentItemIdItemId(str, Enum):
    A = "a"
    B = "b"
    C = "c"

    def __str__(self) -> str:
        return str(self.value)
