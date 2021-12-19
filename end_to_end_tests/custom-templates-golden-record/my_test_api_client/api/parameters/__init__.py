""" Contains methods for accessing the API Endpoints """

import types

from . import (
    delete_common_parameters_overriding_param,
    get_common_parameters_overriding_param,
    get_same_name_multiple_locations_param,
    multiple_path_parameters,
)


class ParametersEndpoints:
    @classmethod
    def get_common_parameters_overriding_param(cls) -> types.ModuleType:
        """
        Test that if you have an overriding property from `PathItem` in `Operation`, it produces valid code
        """
        return get_common_parameters_overriding_param

    @classmethod
    def delete_common_parameters_overriding_param(cls) -> types.ModuleType:
        return delete_common_parameters_overriding_param

    @classmethod
    def get_same_name_multiple_locations_param(cls) -> types.ModuleType:
        return get_same_name_multiple_locations_param

    @classmethod
    def multiple_path_parameters(cls) -> types.ModuleType:
        return multiple_path_parameters
