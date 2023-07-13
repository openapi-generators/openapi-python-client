from typing import Callable, Set, TYPE_CHECKING

if TYPE_CHECKING:
    from openapi_python_client.parser.endpoints import EndpointCollection


TEndpointFilter = Callable[["EndpointCollection"], Set[str]]
