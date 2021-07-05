""" Contains methods for accessing the API Endpoints """

import types

from my_test_api_client.api.tag1 import get_tag_with_number


class Tag1Endpoints:
    @classmethod
    def get_tag_with_number(cls) -> types.ModuleType:
        return get_tag_with_number
