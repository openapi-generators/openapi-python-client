from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple, Union, Iterable

from .. import schema as oai
from .. import utils
from ..config import Config
from .endpoints import Endpoint
from .errors import ParseError
from .properties import Parameters, Schemas, SecurityProperty
from .responses import process_responses


@dataclass
class EndpointCollection:
    """A bunch of endpoints grouped under a tag that will become a module"""

    tag: str
    endpoints: List["Endpoint"] = field(default_factory=list)
    parse_errors: List[ParseError] = field(default_factory=list)

    def endpoints_by_method(self, method: str) -> List[Endpoint]:
        return [e for e in self.endpoints if e.method == method]

    @property
    def endpoints_to_render(self) -> List[Endpoint]:
        return [e for e in self.endpoints if e.has_json_response and (e.is_root_endpoint or e.transformer)]
        # For now only include list endpoints without path parameters
        # return [e for e in self.endpoints if e.list_property and not e.has_path_parameters]

    @property
    def root_endpoints(self) -> List[Endpoint]:
        """All non-transformer endpoints"""
        return [e for e in self.endpoints_to_render if e.is_root_endpoint]

    @property
    def transformer_endpoints(self) -> List[Endpoint]:
        return [e for e in self.endpoints_to_render if e.transformer]

    @property
    def relative_imports(self) -> Set[str]:
        """Relative import strings for all resources in this tag package"""
        return {f"from .{endpoint.python_name} import {endpoint.python_name}" for endpoint in self.endpoints_to_render}

    @property
    def imports_with_tag_prefix(self) -> Set[str]:
        """Relative imports in the form of `from .[tag] import [endpoint_name]`"""
        return {f"from .{self.tag} import {endpoint.python_name}" for endpoint in self.endpoints_to_render}

    @property
    def imports_from_root(self) -> Set[str]:
        return {f"from .api import {endpoint.python_name}" for endpoint in self.endpoints_to_render}

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

        methods = config.include_methods

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


Tree = Dict[str, Union["Endpoint", "Tree"]]


@dataclass
class Endpoints:
    endpoints_by_tag: Dict[utils.PythonIdentifier, EndpointCollection]
    endpoints_by_name: Dict[str, Endpoint]
    endpoints_tree: Tree

    def find_immediate_parent(self, path: str) -> Optional[Endpoint]:
        """Find the parent of the given endpoint.

        Example:
            `find_immediate_parent('/api/v2/ability/{id}') -> Endpoint<'/api/v2/ability'>`
        """
        parts = path.strip("/").split("/")
        while parts:
            current_node = self.endpoints_tree
            parts.pop()
            for part in parts:
                current_node = current_node[part]  # type: ignore
            if "<endpoint>" in current_node:
                return current_node["<endpoint>"]  # type: ignore
        return None

    def find_nearest_list_parent(self, path: str) -> Optional[Endpoint]:
        parts = path.strip("/").split("/")
        while parts:
            current_node = self.endpoints_tree
            parts.pop()
            for part in parts:
                current_node = current_node[part]  # type: ignore
            if parent_endpoint := current_node.get("<endpoint>"):
                if parent_endpoint.list_property:  # type: ignore
                    return parent_endpoint  # type: ignore
        return None

    @staticmethod
    def from_data(
        *,
        data: Dict[str, oai.PathItem],
        schemas: Schemas,
        parameters: Parameters,
        security_schemes: Dict[str, SecurityProperty],
        config: Config,
    ) -> Tuple["Endpoints", Schemas, Parameters]:
        """Parse the openapi paths data to get EndpointCollections by tag"""
        endpoints_by_tag: Dict[utils.PythonIdentifier, EndpointCollection] = {}
        endpoints_by_name: Dict[str, Endpoint] = {}
        tree: Tree = {}

        methods = config.include_methods

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
                endpoints_by_name[endpoint.name] = endpoint
        endpoints_by_tag = dict(sorted(endpoints_by_tag.items(), key=lambda k: k[0]))

        tree = build_endpoint_tree(endpoints_by_name.values())

        ret = Endpoints(endpoints_by_tag, endpoints_by_name, endpoints_tree=tree)

        process_responses(schemas, ret)
        # TODO: Refactor
        for endpoint in endpoints_by_name.values():
            # endpoint.parent = ret.find_immediate_parent(endpoint.path)
            # Set parent to the list endpoint above this endpoint
            endpoint.parent = ret.find_nearest_list_parent(endpoint.path)
        return ret, schemas, parameters


def build_endpoint_tree(endpoints: Iterable[Endpoint]) -> Tree:
    tree: Tree = {}
    for endpoint in endpoints:
        path = endpoint.path
        parts = path.strip("/").split("/")
        current_node = tree
        for part in parts:
            if part not in current_node:
                current_node[part] = {}
            current_node = current_node[part]  # type: ignore
        current_node["<endpoint>"] = endpoint
    return tree
