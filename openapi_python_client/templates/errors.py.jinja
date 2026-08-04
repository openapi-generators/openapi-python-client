"""Contains shared errors types that can be raised from API functions"""

from typing import Any


class UnexpectedStatus(Exception):
    """Raised by api functions when the response status is not part of the normal return path.

    A status documented in the source OpenAPI document as anything other than a success carries its parsed body on
    `parsed`. An undocumented status -- raised only when Client.raise_on_unexpected_status is True -- leaves `parsed`
    as None, since there is no schema to parse it against. The raw body is always on `content`.
    """

    def __init__(self, status_code: int, content: bytes, parsed: Any = None):
        self.status_code = status_code
        self.content = content
        self.parsed = parsed

        # The body is left out of the message on purpose: it may contain PHI, and exception text reaches
        # logs and tracebacks. A caller that needs the body reads it off ``content`` or ``parsed``.
        super().__init__(f"Unexpected status code: {status_code}")


__all__ = ["UnexpectedStatus"]
