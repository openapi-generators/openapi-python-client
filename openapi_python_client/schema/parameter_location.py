from enum import StrEnum


class ParameterLocation(StrEnum):
    """The places Parameters can be put when calling an Endpoint"""

    QUERY = "query"
    PATH = "path"
    HEADER = "header"
    COOKIE = "cookie"
