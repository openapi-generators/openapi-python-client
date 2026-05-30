"""Contains methods for accessing the API"""

from .bodies import BodiesEndpoints
from .config import ConfigEndpoints
from .default import DefaultEndpoints
from .defaults import DefaultsEndpoints
from .enums import EnumsEndpoints
from .location import LocationEndpoints
from .naming import NamingEndpoints
from .parameter_references import ParameterReferencesEndpoints
from .parameters import ParametersEndpoints
from .responses import ResponsesEndpoints
from .tag1 import Tag1Endpoints
from .tag2 import Tag2Endpoints
from .tests import TestsEndpoints
from .true_ import True_Endpoints


class MyTestApiClientApi:
    @classmethod
    def bodies(cls) -> type[BodiesEndpoints]:
        return BodiesEndpoints

    @classmethod
    def tests(cls) -> type[TestsEndpoints]:
        return TestsEndpoints

    @classmethod
    def defaults(cls) -> type[DefaultsEndpoints]:
        return DefaultsEndpoints

    @classmethod
    def enums(cls) -> type[EnumsEndpoints]:
        return EnumsEndpoints

    @classmethod
    def responses(cls) -> type[ResponsesEndpoints]:
        return ResponsesEndpoints

    @classmethod
    def default(cls) -> type[DefaultEndpoints]:
        return DefaultEndpoints

    @classmethod
    def parameters(cls) -> type[ParametersEndpoints]:
        return ParametersEndpoints

    @classmethod
    def tag1(cls) -> type[Tag1Endpoints]:
        return Tag1Endpoints

    @classmethod
    def tag2(cls) -> type[Tag2Endpoints]:
        return Tag2Endpoints

    @classmethod
    def location(cls) -> type[LocationEndpoints]:
        return LocationEndpoints

    @classmethod
    def true_(cls) -> type[True_Endpoints]:
        return True_Endpoints

    @classmethod
    def naming(cls) -> type[NamingEndpoints]:
        return NamingEndpoints

    @classmethod
    def parameter_references(cls) -> type[ParameterReferencesEndpoints]:
        return ParameterReferencesEndpoints

    @classmethod
    def config(cls) -> type[ConfigEndpoints]:
        return ConfigEndpoints
