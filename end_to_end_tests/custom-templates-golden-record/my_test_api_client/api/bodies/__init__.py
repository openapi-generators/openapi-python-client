"""Contains methods for accessing the API Endpoints"""

import types

from . import json_like, post_bodies_multiple


class BodiesEndpoints:
    @classmethod
    def post_bodies_multiple(cls) -> types.ModuleType:
        """
        Test multiple bodies
        """
        return post_bodies_multiple

    @classmethod
    def json_like(cls) -> types.ModuleType:
        """
        A content type that works like json but isn't application/json
        """
        return json_like
