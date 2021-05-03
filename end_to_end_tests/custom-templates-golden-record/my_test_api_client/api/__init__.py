""" Contains methods for accessing the API """


from typing import Type

from my_test_api_client.api.default import DefaultEndpoints
from my_test_api_client.api.tests import TestsEndpoints


class MyTestApiClientApi:
    @classmethod
    def tests(cls) -> Type[TestsEndpoints]:
        return TestsEndpoints

    @classmethod
    def default(cls) -> Type[DefaultEndpoints]:
        return DefaultEndpoints
