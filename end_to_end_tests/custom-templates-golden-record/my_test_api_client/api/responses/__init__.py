"""Contains methods for accessing the API Endpoints"""

import types

from . import default_response, post_responses_unions_simple_before_complex, reference_response, text_response


class ResponsesEndpoints:
    @classmethod
    def post_responses_unions_simple_before_complex(cls) -> types.ModuleType:
        """
        Regression test for #603
        """
        return post_responses_unions_simple_before_complex

    @classmethod
    def text_response(cls) -> types.ModuleType:
        """
        Text Response
        """
        return text_response

    @classmethod
    def default_response(cls) -> types.ModuleType:
        """
        Default Response
        """
        return default_response

    @classmethod
    def reference_response(cls) -> types.ModuleType:
        """
        Endpoint using predefined response
        """
        return reference_response
