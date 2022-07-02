""" Contains methods for accessing the API Endpoints """

import types

from . import post_responses_unions_simple_before_complex


class ResponsesEndpoints:
    @classmethod
    def post_responses_unions_simple_before_complex(cls) -> types.ModuleType:
        """
        Regression test for #603
        """
        return post_responses_unions_simple_before_complex
