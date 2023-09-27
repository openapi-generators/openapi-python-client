from enum import Enum
from typing import Union


class AnotherAllOfSubModelType(str, Enum):
    SUBMODEL = "submodel"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def from_val(cls, value: Union[str, "AnotherAllOfSubModelType"]) -> "AnotherAllOfSubModelType":
        if isinstance(value, AnotherAllOfSubModelType):
            return value

        value = value.lower()

        for enum in cls:
            if enum.value.lower() == value:
                return enum

        return AnotherAllOfSubModelType(value)
