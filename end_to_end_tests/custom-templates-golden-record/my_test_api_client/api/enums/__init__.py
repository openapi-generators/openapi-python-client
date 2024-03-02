"""Contains methods for accessing the API Endpoints"""

import types

from . import bool_enum_tests_bool_enum_post, int_enum_tests_int_enum_post


class EnumsEndpoints:
    @classmethod
    def int_enum_tests_int_enum_post(cls) -> types.ModuleType:
        """
        Int Enum
        """
        return int_enum_tests_int_enum_post

    @classmethod
    def bool_enum_tests_bool_enum_post(cls) -> types.ModuleType:
        """
        Bool Enum
        """
        return bool_enum_tests_bool_enum_post
