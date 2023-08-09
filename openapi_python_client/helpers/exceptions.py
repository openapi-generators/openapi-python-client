"""Defines a common set of exceptions which developers can raise and/or catch."""

from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    import requests


class FatalAPIError(Exception):
    """Exception raised when a failed request should not be considered retriable."""


class RetriableAPIError(Exception):
    """Exception raised when a failed request can be safely retried."""

    def __init__(self, message: str, response: "requests.Response" | None = None) -> None:
        """Extends the default with the failed response as an attribute.

        Args:
            message (str): The Error Message
            response (requests.Response): The response object.
        """
        super().__init__(message)
        self.response = response
