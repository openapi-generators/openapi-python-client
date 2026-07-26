"""Contains methods for accessing the API Endpoints"""

import types

from . import hyphen_in_path, mixed_case, post_naming_property_conflict_with_import


class NamingEndpoints:
    @classmethod
    def post_naming_property_conflict_with_import(cls) -> types.ModuleType:
        return post_naming_property_conflict_with_import

    @classmethod
    def mixed_case(cls) -> types.ModuleType:
        return mixed_case

    @classmethod
    def hyphen_in_path(cls) -> types.ModuleType:
        return hyphen_in_path
