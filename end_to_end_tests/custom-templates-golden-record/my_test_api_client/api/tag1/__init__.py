""" Contains methods for accessing the API Endpoints """

import types

from . import get_tag_with_number


class Tag1Endpoints:
    @classmethod
    def get_tag_with_number(cls) -> types.ModuleType:
        return get_tag_with_number
