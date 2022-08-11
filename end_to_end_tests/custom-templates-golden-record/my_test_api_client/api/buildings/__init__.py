""" Contains methods for accessing the API Endpoints """

import types

from . import get_v1_buildings


class BuildingsEndpoints:
    @classmethod
    def get_v1_buildings(cls) -> types.ModuleType:
        """
        Search for sorted and paged buildings
        """
        return get_v1_buildings
