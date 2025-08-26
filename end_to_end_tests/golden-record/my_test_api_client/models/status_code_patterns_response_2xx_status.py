from enum import Enum


class StatusCodePatternsResponse2XXStatus(str, Enum):
    FAILURE = "failure"
    SUCCESS = "success"

    def __str__(self) -> str:
        return str(self.value)
