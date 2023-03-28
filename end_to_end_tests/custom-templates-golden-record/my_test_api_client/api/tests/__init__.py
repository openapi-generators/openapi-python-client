""" Contains methods for accessing the API Endpoints """

import types

from . import (
    callback_test,
    defaults_tests_defaults_post,
    description_with_backslash,
    get_basic_list_of_booleans,
    get_basic_list_of_floats,
    get_basic_list_of_integers,
    get_basic_list_of_strings,
    get_user_list,
    int_enum_tests_int_enum_post,
    json_body_tests_json_body_post,
    no_response_tests_no_response_get,
    octet_stream_tests_octet_stream_get,
    post_form_data,
    post_form_data_inline,
    post_tests_json_body_string,
    test_inline_objects,
    token_with_cookie_auth_token_with_cookie_get,
    unsupported_content_tests_unsupported_content_get,
    upload_file_tests_upload_post,
    upload_multiple_files_tests_upload_post,
)


class TestsEndpoints:
    @classmethod
    def get_user_list(cls) -> types.ModuleType:
        """
        Get a list of things
        """
        return get_user_list

    @classmethod
    def get_basic_list_of_strings(cls) -> types.ModuleType:
        """
        Get a list of strings
        """
        return get_basic_list_of_strings

    @classmethod
    def get_basic_list_of_integers(cls) -> types.ModuleType:
        """
        Get a list of integers
        """
        return get_basic_list_of_integers

    @classmethod
    def get_basic_list_of_floats(cls) -> types.ModuleType:
        """
        Get a list of floats
        """
        return get_basic_list_of_floats

    @classmethod
    def get_basic_list_of_booleans(cls) -> types.ModuleType:
        """
        Get a list of booleans
        """
        return get_basic_list_of_booleans

    @classmethod
    def post_form_data(cls) -> types.ModuleType:
        """
        Post form data
        """
        return post_form_data

    @classmethod
    def post_form_data_inline(cls) -> types.ModuleType:
        """
        Post form data (inline schema)
        """
        return post_form_data_inline

    @classmethod
    def upload_file_tests_upload_post(cls) -> types.ModuleType:
        """
        Upload a file
        """
        return upload_file_tests_upload_post

    @classmethod
    def upload_multiple_files_tests_upload_post(cls) -> types.ModuleType:
        """
        Upload several files in the same request
        """
        return upload_multiple_files_tests_upload_post

    @classmethod
    def json_body_tests_json_body_post(cls) -> types.ModuleType:
        """
        Try sending a JSON body
        """
        return json_body_tests_json_body_post

    @classmethod
    def post_tests_json_body_string(cls) -> types.ModuleType:
        """
        Json Body Which is String
        """
        return post_tests_json_body_string

    @classmethod
    def defaults_tests_defaults_post(cls) -> types.ModuleType:
        """
        Defaults
        """
        return defaults_tests_defaults_post

    @classmethod
    def octet_stream_tests_octet_stream_get(cls) -> types.ModuleType:
        """
        Octet Stream
        """
        return octet_stream_tests_octet_stream_get

    @classmethod
    def no_response_tests_no_response_get(cls) -> types.ModuleType:
        """
        No Response
        """
        return no_response_tests_no_response_get

    @classmethod
    def unsupported_content_tests_unsupported_content_get(cls) -> types.ModuleType:
        """
        Unsupported Content
        """
        return unsupported_content_tests_unsupported_content_get

    @classmethod
    def int_enum_tests_int_enum_post(cls) -> types.ModuleType:
        """
        Int Enum
        """
        return int_enum_tests_int_enum_post

    @classmethod
    def test_inline_objects(cls) -> types.ModuleType:
        """
        Test Inline Objects
        """
        return test_inline_objects

    @classmethod
    def token_with_cookie_auth_token_with_cookie_get(cls) -> types.ModuleType:
        """
        Test optional cookie parameters
        """
        return token_with_cookie_auth_token_with_cookie_get

    @classmethod
    def callback_test(cls) -> types.ModuleType:
        """
        Try sending a request related to a callback
        """
        return callback_test

    @classmethod
    def description_with_backslash(cls) -> types.ModuleType:
        """
            Test description with \
        """
        return description_with_backslash
