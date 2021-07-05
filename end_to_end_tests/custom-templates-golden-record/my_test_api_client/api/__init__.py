""" Contains methods for accessing the API """

from typing import Type

from my_test_api_client.api.default import DefaultEndpoints
from my_test_api_client.api.parameters import ParametersEndpoints
from my_test_api_client.api.tag1 import Tag1Endpoints
from my_test_api_client.api.tests import TestsEndpoints


class MyTestApiClientApi:
    @classmethod
    def tests(cls) -> Type[TestsEndpoints]:
        return TestsEndpoints

    @classmethod
    def default(cls) -> Type[DefaultEndpoints]:
        return DefaultEndpoints

    @classmethod
    def parameters(cls) -> Type[ParametersEndpoints]:
        return ParametersEndpoints

    @classmethod
    def tag1(cls) -> Type[Tag1Endpoints]:
        return Tag1Endpoints
