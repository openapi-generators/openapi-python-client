"""Contains methods for accessing the API Endpoints"""

import types

from . import json_like, optional_body, post_bodies_multiple, post_bodies_multiple_required, refs


class BodiesEndpoints:
    @classmethod
    def post_bodies_multiple(cls) -> types.ModuleType:
        """
        Test multiple bodies
        """
        return post_bodies_multiple

    @classmethod
    def post_bodies_multiple_required(cls) -> types.ModuleType:
        """
        Test multiple bodies, all required
        """
        return post_bodies_multiple_required

    @classmethod
    def json_like(cls) -> types.ModuleType:
        """
        A content type that works like json but isn't application/json
        """
        return json_like

    @classmethod
    def refs(cls) -> types.ModuleType:
        """
        Test request body defined via ref
        """
        return refs

    @classmethod
    def optional_body(cls) -> types.ModuleType:
        """
        Test optional request body
        """
        return optional_body
