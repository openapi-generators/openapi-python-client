""" Contains methods for accessing the API Endpoints """

import types

from . import post_naming_property_conflict_with_import


class NamingEndpoints:
    @classmethod
    def post_naming_property_conflict_with_import(cls) -> types.ModuleType:
        return post_naming_property_conflict_with_import
