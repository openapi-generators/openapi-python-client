"""Contains methods for accessing the API Endpoints"""

import types

from . import (
    default_status_code,
    get_responses_unions_any_or_string,
    get_responses_unions_branded_or_model,
    get_responses_unions_int_or_bool,
    get_responses_unions_model_or_null,
    get_responses_unions_model_or_string,
    get_responses_unions_number_or_string,
    get_responses_unions_object_or_string,
    get_responses_unions_scalars,
    jsonl_stream,
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
    def get_responses_unions_scalars(cls) -> types.ModuleType:
        """
        A union of scalar types.
        """
        return get_responses_unions_scalars

    @classmethod
    def get_responses_unions_number_or_string(cls) -> types.ModuleType:
        """
        A union with a `number` member: JSON draws no int/float distinction, so an integer body is valid.
        """
        return get_responses_unions_number_or_string

    @classmethod
    def get_responses_unions_int_or_bool(cls) -> types.ModuleType:
        """
        A union whose Python type collapses to `int`, since `bool` is a subclass of it.
        """
        return get_responses_unions_int_or_bool

    @classmethod
    def get_responses_unions_model_or_string(cls) -> types.ModuleType:
        """
        A union mixing a model with a raw value.
        """
        return get_responses_unions_model_or_string

    @classmethod
    def get_responses_unions_model_or_null(cls) -> types.ModuleType:
        """
        A nullable model: every non-null body must parse as the model or be rejected.
        """
        return get_responses_unions_model_or_null

    @classmethod
    def get_responses_unions_object_or_string(cls) -> types.ModuleType:
        """
        A union mixing a free-form object with a raw value.
        """
        return get_responses_unions_object_or_string

    @classmethod
    def get_responses_unions_any_or_string(cls) -> types.ModuleType:
        """
        A union with an untyped member, which accepts any body at all.
        """
        return get_responses_unions_any_or_string

    @classmethod
    def get_responses_unions_branded_or_model(cls) -> types.ModuleType:
        """
        A union with a branded string member, which arrives as a plain JSON string.
        """
        return get_responses_unions_branded_or_model

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
    def jsonl_stream(cls) -> types.ModuleType:
        """
        A streaming response, plus a documented error status the stream can end on instead.
        """
        return jsonl_stream

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
