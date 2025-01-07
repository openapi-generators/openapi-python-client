from enum import Enum


class AnotherAllOfSubModelType(str, Enum):
    SUBMODEL = "submodel"

    def __str__(self) -> str:
        return str(self.value)
