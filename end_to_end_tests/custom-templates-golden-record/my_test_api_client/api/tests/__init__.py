""" Contains methods for accessing the API Endpoints """


import types

from my_test_api_client.api.tests import (
    defaults_tests_defaults_post,
    get_basic_list_of_booleans,
    get_basic_list_of_floats,
    get_basic_list_of_integers,
    get_basic_list_of_strings,
    get_user_list,
    int_enum_tests_int_enum_post,
    json_body_tests_json_body_post,
    no_response_tests_no_response_get,
    octet_stream_tests_octet_stream_get,
    optional_value_tests_optional_query_param,
    test_inline_objects,
    token_with_cookie_auth_token_with_cookie_get,
    unsupported_content_tests_unsupported_content_get,
    upload_file_tests_upload_post,
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
    def upload_file_tests_upload_post(cls) -> types.ModuleType:
        """
        Upload a file
        """
        return upload_file_tests_upload_post

    @classmethod
    def json_body_tests_json_body_post(cls) -> types.ModuleType:
        """
        Try sending a JSON body
        """
        return json_body_tests_json_body_post

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
    def optional_value_tests_optional_query_param(cls) -> types.ModuleType:
        """
        Test optional query parameters
        """
        return optional_value_tests_optional_query_param

    @classmethod
    def token_with_cookie_auth_token_with_cookie_get(cls) -> types.ModuleType:
        """
        Test optional cookie parameters
        """
        return token_with_cookie_auth_token_with_cookie_get
