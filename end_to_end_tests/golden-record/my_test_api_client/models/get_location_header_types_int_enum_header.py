from enum import IntEnum
from typing import Union


class GetLocationHeaderTypesIntEnumHeader(IntEnum):
    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def from_val(
        cls, value: Union[int, str, "GetLocationHeaderTypesIntEnumHeader"]
    ) -> "GetLocationHeaderTypesIntEnumHeader":
        if isinstance(value, GetLocationHeaderTypesIntEnumHeader):
            return value

        if isinstance(value, str):
            value = value.lower()
            for key in cls.__members__.keys():
                if key.lower() == value:
                    return cls[key]

            # try to convert value to int
            try:
                value = int(value)
            except ValueError:
                pass

        return cls(value)
