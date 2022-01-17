""" Contains methods for accessing the API Endpoints """

import types

from . import get_location_header_types, get_location_query_optionality


class LocationEndpoints:
    @classmethod
    def get_location_query_optionality(cls) -> types.ModuleType:
        return get_location_query_optionality

    @classmethod
    def get_location_header_types(cls) -> types.ModuleType:
        return get_location_header_types
