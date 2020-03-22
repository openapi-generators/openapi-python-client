from httpx import Response


class ApiResponseError(Exception):
    """ An exception raised when an unknown response occurs """

    def __init__(self, *, response: Response):
        super().__init__()
        self.response: Response = response
