""" Contains methods for accessing the API Endpoints """

import types

from . import get_common_parameters, post_common_parameters


class DefaultEndpoints:
    @classmethod
    def get_common_parameters(cls) -> types.ModuleType:
        return get_common_parameters

    @classmethod
    def post_common_parameters(cls) -> types.ModuleType:
        return post_common_parameters
