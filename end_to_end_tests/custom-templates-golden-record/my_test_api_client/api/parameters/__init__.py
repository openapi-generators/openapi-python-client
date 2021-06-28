""" Contains methods for accessing the API Endpoints """

import types

from my_test_api_client.api.parameters import get_same_name_multiple_locations_param


class ParametersEndpoints:
    @classmethod
    def get_same_name_multiple_locations_param(cls) -> types.ModuleType:
        return get_same_name_multiple_locations_param
