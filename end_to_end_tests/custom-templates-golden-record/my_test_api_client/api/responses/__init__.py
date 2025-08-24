"""Contains methods for accessing the API Endpoints"""

import types

from . import (
    default_status_code,
    post_responses_unions_simple_before_complex,
    reference_response,
    status_code_patterns,
    status_code_precedence,
    text_response,
)


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
    def reference_response(cls) -> types.ModuleType:
        """
        Endpoint using predefined response
        """
        return reference_response

    @classmethod
    def default_status_code(cls) -> types.ModuleType:
        """
        Default Status Code Only
        """
        return default_status_code

    @classmethod
    def status_code_patterns(cls) -> types.ModuleType:
        """
        Status Code Patterns
        """
        return status_code_patterns

    @classmethod
    def status_code_precedence(cls) -> types.ModuleType:
        """
        Verify that specific status codes are always checked first, then ranges, then default
        """
        return status_code_precedence
