from enum import Enum
from typing import Literal


class AnAllOfEnum(str, Enum):
    A_DEFAULT = "a_default"
    BAR = "bar"
    FOO = "foo"
    OVERRIDDEN_DEFAULT = "overridden_default"

    def __str__(self) -> str:
        return str(self.value)


AnAllOfEnumLiteral = Literal[
    "a_default",
    "bar",
    "foo",
    "overridden_default",
]
