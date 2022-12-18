""" Contains shared errors types that can be raised from API functions """


class UnexpectedStatus(Exception):
    """Raised by api functions when the response status an undocumented status and Client.raise_on_unexpected_status is True"""

    ...


__all__ = ["UnexpectedStatus"]
