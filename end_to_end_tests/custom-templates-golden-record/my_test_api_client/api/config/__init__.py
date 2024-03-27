"""Contains methods for accessing the API Endpoints"""

import types

from . import content_type_override


class ConfigEndpoints:
    @classmethod
    def content_type_override(cls) -> types.ModuleType:
        """
        Content Type Override
        """
        return content_type_override
