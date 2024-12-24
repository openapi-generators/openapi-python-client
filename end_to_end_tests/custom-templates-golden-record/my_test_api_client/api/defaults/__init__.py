"""Contains methods for accessing the API Endpoints"""

import types

from . import defaults_tests_defaults_post


class DefaultsEndpoints:
    @classmethod
    def defaults_tests_defaults_post(cls) -> types.ModuleType:
        """
        Defaults
        """
        return defaults_tests_defaults_post
