""" Contains shared errors types that can be raised from API functions """


class UnexpectedStatus(Exception):
    """Raised by api functions when the response status is undocumented and Client.raise_on_unexpected_status is True"""


class ErrorStatus(Exception):
    """Raised by api functions when the response status marks an error"""


class ExpectedErrorStatus(ErrorStatus):
    pass


class UnexpectedErrorStatus(ErrorStatus, UnexpectedStatus):
    pass


class UnexpectedSuccessStatus(UnexpectedStatus):
    pass


__all__ = [
    "ErrorStatus",
    "ExpectedErrorStatus",
    "UnexpectedErrorStatus",
    "UnexpectedStatus",
    "UnexpectedSuccessStatus",
]
