from enum import StrEnum


class AnotherAllOfSubModelType(StrEnum):
    SUBMODEL = "submodel"

    def __str__(self) -> str:
        return str(self.value)
