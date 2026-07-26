from enum import StrEnum


class ModelWithMergedPropertiesStringToEnum(StrEnum):
    A = "a"
    B = "b"

    def __str__(self) -> str:
        return str(self.value)
