""" Contains methods for accessing the API Endpoints """

import types

from . import (
    delete_common_parameters_overriding_param,
    get_common_parameters_overriding_param,
    get_same_name_multiple_locations_param,
)


class ParametersEndpoints:
    @classmethod
    def get_common_parameters_overriding_param(cls) -> types.ModuleType:
        return get_common_parameters_overriding_param

    @classmethod
    def delete_common_parameters_overriding_param(cls) -> types.ModuleType:
        return delete_common_parameters_overriding_param

    @classmethod
    def get_same_name_multiple_locations_param(cls) -> types.ModuleType:
        return get_same_name_multiple_locations_param
