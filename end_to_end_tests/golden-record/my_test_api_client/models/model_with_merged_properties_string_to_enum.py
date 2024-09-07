from enum import Enum


class ModelWithMergedPropertiesStringToEnum(str, Enum):
    A = "a"
    B = "b"

    def __str__(self) -> str:
        return str(self.value)
