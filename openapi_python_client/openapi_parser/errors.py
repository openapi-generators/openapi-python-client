from typing import Any, Optional


class ParseError(ValueError):
    """ An error raised when there's a problem parsing an OpenAPI document """

    def __init__(self, data: Any, message: Optional[str] = None):
        super().__init__()
        self.data = data
        self.message = message
