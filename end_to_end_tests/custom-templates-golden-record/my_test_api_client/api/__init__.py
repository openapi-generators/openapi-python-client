""" Contains methods for accessing the API """

from typing import Type

from .default import DefaultEndpoints
from .location import LocationEndpoints
from .parameter_references import ParameterReferencesEndpoints
from .parameters import ParametersEndpoints
from .responses import ResponsesEndpoints
from .tag1 import Tag1Endpoints
from .tests import TestsEndpoints
from .true_ import True_Endpoints


class MyTestApiClientApi:
    @classmethod
    def tests(cls) -> Type[TestsEndpoints]:
        return TestsEndpoints

    @classmethod
    def responses(cls) -> Type[ResponsesEndpoints]:
        return ResponsesEndpoints

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
    def true_(cls) -> Type[True_Endpoints]:
        return True_Endpoints

    @classmethod
    def parameter_references(cls) -> Type[ParameterReferencesEndpoints]:
        return ParameterReferencesEndpoints
