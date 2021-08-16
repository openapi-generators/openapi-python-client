""" Contains methods for accessing the API """

from typing import Type

from .default import DefaultEndpoints
from .location import LocationEndpoints
from .naming import NamingEndpoints
from .parameters import ParametersEndpoints
from .tag1 import Tag1Endpoints
from .tests import TestsEndpoints


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

    @classmethod
    def location(cls) -> Type[LocationEndpoints]:
        return LocationEndpoints

    @classmethod
    def naming(cls) -> Type[NamingEndpoints]:
        return NamingEndpoints
