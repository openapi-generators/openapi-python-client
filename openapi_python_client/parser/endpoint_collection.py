from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .. import schema as oai
from .. import utils
from ..config import Config
from .properties import Parameters, Schemas, SecurityProperty
from .endpoints import Endpoint
from .errors import ParseError


@dataclass
class EndpointCollection:
    """A bunch of endpoints grouped under a tag that will become a module"""

    tag: str
    endpoints: List["Endpoint"] = field(default_factory=list)
    parse_errors: List[ParseError] = field(default_factory=list)

    @staticmethod
    def from_data(
        *,
        data: Dict[str, oai.PathItem],
        schemas: Schemas,
        parameters: Parameters,
        security_schemes: Dict[str, SecurityProperty],
        config: Config,
    ) -> Tuple[Dict[utils.PythonIdentifier, "EndpointCollection"], Schemas, Parameters]:
        """Parse the openapi paths data to get EndpointCollections by tag"""
        endpoints_by_tag: Dict[utils.PythonIdentifier, EndpointCollection] = {}

        methods = ["get", "put", "post", "delete", "options", "head", "patch", "trace"]

        for path, path_data in data.items():
            for method in methods:
                operation: Optional[oai.Operation] = getattr(path_data, method)
                if operation is None:
                    continue
                tag = utils.PythonIdentifier(value=(operation.tags or ["default"])[0], prefix="tag")
                collection = endpoints_by_tag.setdefault(tag, EndpointCollection(tag=tag))
                endpoint, schemas, parameters = Endpoint.from_data(
                    data=operation,
                    path=path,
                    method=method,
                    tag=tag,
                    schemas=schemas,
                    security_schemes=security_schemes,
                    parameters=parameters,
                    config=config,
                )
                # Add `PathItem` parameters
                if not isinstance(endpoint, ParseError):
                    endpoint, schemas, parameters = Endpoint.add_parameters(
                        endpoint=endpoint, data=path_data, schemas=schemas, parameters=parameters, config=config
                    )
                if not isinstance(endpoint, ParseError):
                    endpoint = Endpoint.sort_parameters(endpoint=endpoint)
                if isinstance(endpoint, ParseError):
                    endpoint.header = (
                        f"WARNING parsing {method.upper()} {path} within {tag}. Endpoint will not be generated."
                    )
                    collection.parse_errors.append(endpoint)
                    continue
                for error in endpoint.errors:
                    error.header = f"WARNING parsing {method.upper()} {path} within {tag}."
                    collection.parse_errors.append(error)
                collection.endpoints.append(endpoint)

        return endpoints_by_tag, schemas, parameters
