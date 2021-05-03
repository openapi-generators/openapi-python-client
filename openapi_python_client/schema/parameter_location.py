from enum import Enum


class ParameterLocation(str, Enum):
    """The places Parameters can be put when calling an Endpoint"""

    QUERY = "query"
    PATH = "path"
    HEADER = "header"
    COOKIE = "cookie"
