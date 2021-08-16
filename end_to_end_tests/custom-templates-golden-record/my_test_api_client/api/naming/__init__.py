""" Contains methods for accessing the API Endpoints """

import types

from . import get_naming_keywords


class NamingEndpoints:
    @classmethod
    def get_naming_keywords(cls) -> types.ModuleType:
        return get_naming_keywords
