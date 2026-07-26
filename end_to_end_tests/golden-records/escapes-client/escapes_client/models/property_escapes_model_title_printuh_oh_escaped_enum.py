from enum import StrEnum


class PropertyEscapesModelTitlePrintuhOhEscapedEnum(StrEnum):
    NORMAL_VALUE = "normal value"
    VALUE_PRINTUH_OH = "value\" + print('uh oh') + \""

    def __str__(self) -> str:
        return str(self.value)
