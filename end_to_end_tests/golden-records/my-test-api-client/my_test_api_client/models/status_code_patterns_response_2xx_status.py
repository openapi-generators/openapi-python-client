from enum import StrEnum


class StatusCodePatternsResponse2XXStatus(StrEnum):
    FAILURE = "failure"
    SUCCESS = "success"

    def __str__(self) -> str:
        return str(self.value)
