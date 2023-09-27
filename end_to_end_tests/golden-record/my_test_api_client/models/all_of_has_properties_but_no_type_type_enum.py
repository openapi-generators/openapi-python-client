from enum import IntEnum
from typing import Union


class AllOfHasPropertiesButNoTypeTypeEnum(IntEnum):
    VALUE_0 = 0
    VALUE_1 = 1

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def from_val(
        cls, value: Union[int, str, "AllOfHasPropertiesButNoTypeTypeEnum"]
    ) -> "AllOfHasPropertiesButNoTypeTypeEnum":
        if isinstance(value, AllOfHasPropertiesButNoTypeTypeEnum):
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
