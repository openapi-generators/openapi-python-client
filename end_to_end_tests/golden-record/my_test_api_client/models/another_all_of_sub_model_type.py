from enum import Enum
from typing import Literal


class AnotherAllOfSubModelType(str, Enum):
    SUBMODEL = "submodel"

    def __str__(self) -> str:
        return str(self.value)


AnotherAllOfSubModelTypeLiteral = Literal["submodel",]
