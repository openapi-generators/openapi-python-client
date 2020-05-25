from typing import Any, List, Optional


class ParseError(ValueError):
    """ An error raised when there's a problem parsing an OpenAPI document """

    def __init__(
        self,
        data: Any,
        header: str = "ERROR: Unable to parse this part of your OpenAPI document: ",
        message: Optional[str] = None,
    ):
        super().__init__()
        self.data = data
        self.message = message
        self.header = header


class MultipleParseError(ValueError):
    """ Higher level error combining multiple ParseErrors """

    def __init__(self, parse_errors: List[ParseError]):
        super().__init__()
        self.parse_errors = parse_errors
