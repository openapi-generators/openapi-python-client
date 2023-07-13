from typing import Callable, Set, TYPE_CHECKING

if TYPE_CHECKING:
    from parser.endpoints import EndpointCollection


TEndpointFilter = Callable[["EndpointCollection"], Set[str]]
