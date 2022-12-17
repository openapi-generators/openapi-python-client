""" Contains methods for accessing the API Endpoints """

import types

from . import get_parameter_references_path_param


class ParameterReferencesEndpoints:
    @classmethod
    def get_parameter_references_path_param(cls) -> types.ModuleType:
        """
        Test different types of parameter references
        """
        return get_parameter_references_path_param
