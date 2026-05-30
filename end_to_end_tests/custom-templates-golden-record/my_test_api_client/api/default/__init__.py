"""Contains methods for accessing the API Endpoints"""

import types

from . import (
    get_common_parameters,
    get_models_allof,
    get_models_oneof_with_required_const,
    post_common_parameters,
    post_types_unions_duplicate_types,
    reserved_parameters,
)


class DefaultEndpoints:
    @classmethod
    def get_common_parameters(cls) -> types.ModuleType:
        return get_common_parameters

    @classmethod
    def post_common_parameters(cls) -> types.ModuleType:
        return post_common_parameters

    @classmethod
    def reserved_parameters(cls) -> types.ModuleType:
        return reserved_parameters

    @classmethod
    def get_models_allof(cls) -> types.ModuleType:
        return get_models_allof

    @classmethod
    def get_models_oneof_with_required_const(cls) -> types.ModuleType:
        return get_models_oneof_with_required_const

    @classmethod
    def post_types_unions_duplicate_types(cls) -> types.ModuleType:
        return post_types_unions_duplicate_types
