from enum import Enum


class AnAllOfEnum(str, Enum):
    FOO = "foo"
    BAR = "bar"
    A_DEFAULT = "a_default"
    OVERRIDDEN_DEFAULT = "overridden_default"

    def __str__(self) -> str:
        return str(self.value)
