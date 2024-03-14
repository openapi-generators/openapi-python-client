from enum import Enum


class OneOfBlockWithReferencesType0(str, Enum):
    ONEOFBLOCKONE = "OneOfBlockOne"

    def __str__(self) -> str:
        return str(self.value)
