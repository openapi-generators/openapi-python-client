from __future__ import annotations

from typing import Optional, Literal, cast, Union, List, Dict, Any, Iterable, Tuple, Set

from dataclasses import dataclass

import openapi_schema_pydantic as osp

from openapi_python_client.parser.context import OpenapiContext
from openapi_python_client.parser.paths import table_names_from_paths
from openapi_python_client.parser.models import SchemaWrapper, DataPropertyPath, TSchemaType
from openapi_python_client.utils import PythonIdentifier
from openapi_python_client.parser.responses import process_responses
from openapi_python_client.parser.credentials import CredentialsProperty
from openapi_python_client.parser.pagination import Pagination

TMethod = Literal["get", "post", "put", "patch"]
TParamIn = Literal["query", "header", "path", "cookie"]
Tree = Dict[str, Union["Endpoint", "Tree"]]


@dataclass
class TransformerSetting:
    parent_endpoint: Endpoint
    parent_property: DataPropertyPath
    path_parameter: Parameter


@dataclass
class Parameter:
    name: str
    description: Optional[str]
    schema: SchemaWrapper
    raw_schema: osp.Parameter
    required: bool
    location: TParamIn
    python_name: PythonIdentifier
    explode: bool
    style: Optional[str] = None

    def get_imports(self) -> List[str]:
        imports = []
        if self.schema.is_union:
            imports.append("from typing import Union")
        return imports

    @property
    def types(self) -> List[TSchemaType]:
        return self.schema.types

    @property
    def template(self) -> str:
        return self.schema.property_template

    @property
    def default(self) -> Optional[Any]:
        return self.schema.default

    @property
    def nullable(self) -> bool:
        return self.schema.nullable

    def to_string(self) -> str:
        type_hint = self.schema.type_hint
        default = self.default
        if default is None and not self.required:
            default = "UNSET"
        if self.nullable:
            type_hint = f"Optional[{type_hint}]"

        base_string = f"{self.python_name}: {type_hint}"
        if default is not None:
            base_string += f" = {default}"
        return base_string

    def to_docstring(self) -> str:
        doc = f"{self.python_name}: {self.description or ''}"
        if self.default:
            doc += f" Default: {self.default}."
        # TODO: Example
        return doc

    @classmethod
    def from_reference(cls, param_ref: Union[osp.Reference, osp.Parameter], context: OpenapiContext) -> "Parameter":
        osp_param = context.parameter_from_reference(param_ref)
        schema = SchemaWrapper.from_reference(osp_param.param_schema, context)
        description = param_ref.description or osp_param.description or schema.description
        location = osp_param.param_in
        required = osp_param.required

        return cls(
            name=osp_param.name,
            description=description,
            raw_schema=osp_param,
            schema=schema,
            location=cast(TParamIn, location),
            required=required,
            python_name=PythonIdentifier(osp_param.name, prefix=context.config.field_prefix),
            explode=osp_param.explode or False,
            style=osp_param.style,
        )


@dataclass
class Response:
    status_code: str
    description: str
    raw_schema: osp.Response
    content_schema: Optional[SchemaWrapper]
    list_property: Optional[DataPropertyPath] = None

    @property
    def has_content(self) -> bool:
        """Whether this is a no-content response"""
        return bool(self.content_schema)
        # return bool(self.content_schema and self.content_schema.has_properties)

    @property
    def list_properties(self) -> Dict[Tuple[str, ...], SchemaWrapper]:
        """Paths to list properties"""
        if not self.content_schema:
            return {}
        return self.content_schema.crawled_properties.list_properties

    @property
    def object_properties(self) -> Dict[Tuple[str, ...], SchemaWrapper]:
        """Paths to object properties"""
        if not self.content_schema:
            return {}
        return self.content_schema.crawled_properties.object_properties

    @classmethod
    def from_reference(
        cls, status_code: str, resp_ref: Union[osp.Reference, osp.Response], context: OpenapiContext
    ) -> "Response":
        raw_schema = context.response_from_reference(resp_ref)
        description = resp_ref.description or raw_schema.description

        content_schema: Optional[SchemaWrapper] = None
        for content_type, media_type in (raw_schema.content or {}).items():
            # Look for json responses only
            if (content_type == "application/json" or content_type.endswith("+json")) and media_type.media_type_schema:
                content_schema = SchemaWrapper.from_reference(media_type.media_type_schema, context)

        return cls(
            status_code=status_code, description=description, raw_schema=raw_schema, content_schema=content_schema
        )


@dataclass(kw_only=True)
class Endpoint:
    method: TMethod
    responses: dict[str, Response]
    path: str
    parameters: Dict[str, Parameter]
    path_table_name: str
    """Table name inferred from path"""
    raw_schema: osp.Operation

    operation_id: str

    python_name: PythonIdentifier
    credentials: Optional[CredentialsProperty]

    parent: Optional["Endpoint"] = None

    summary: Optional[str] = None
    description: Optional[str] = None

    path_summary: Optional[str] = None
    """Summary applying to all methods of the path"""
    path_description: Optional[str] = None
    """Description applying to all methods of the path"""

    rank: int = 0

    def get_imports(self) -> List[str]:
        """Get all import strings required to use this endpoint"""
        imports: List[str] = []
        if self.credentials:
            imports.extend(self.credentials.get_imports())
        for param in self.parameters.values():
            imports.extend(param.get_imports())
        return imports

    def to_docstring(self) -> str:
        lines = [self.path_summary, self.summary, self.path_description, self.description]
        return "\n".join(line for line in lines if line)

    @property
    def path_parameters(self) -> Dict[str, Parameter]:
        return {p.name: p for p in self.parameters.values() if p.location == "path"}

    @property
    def query_parameters(self) -> Dict[str, Parameter]:
        return {p.name: p for p in self.parameters.values() if p.location == "query"}

    @property
    def header_parameters(self) -> Dict[str, Parameter]:
        return {p.name: p for p in self.parameters.values() if p.location == "header"}

    @property
    def cookie_parameters(self) -> Dict[str, Parameter]:
        return {p.name: p for p in self.parameters.values() if p.location == "cookie"}

    @property
    def list_all_parameters(self) -> List[Parameter]:
        return list(self.parameters.values())

    @property
    def required_parameters(self) -> Dict[str, Parameter]:
        return {name: p for name, p in self.parameters.items() if p.required}

    @property
    def optional_parameters(self) -> Dict[str, Parameter]:
        return {name: p for name, p in self.parameters.items() if not p.required}

    @property
    def request_args_meta(self) -> Dict[str, Dict[str, Dict[str, str]]]:
        """Mapping of how to translate python arguments to request parameters"""
        result: Dict[str, Any] = {}
        for param in self.parameters.values():
            items = result.setdefault(param.location, {})
            items[param.python_name] = {
                "name": param.name,
                "types": param.types,
                "explode": param.explode,
                "style": param.style,
            }
        return result

    @property
    def request_args_meta_str(self) -> str:
        return repr(self.request_args_meta)

    @property
    def data_response(self) -> Optional[Response]:
        if not self.responses:
            return None
        keys = list(self.responses.keys())
        if len(keys) == 1:
            return self.responses[keys[0]]
        success_codes = [k for k in keys if k.startswith("20")]
        if success_codes:
            return self.responses[success_codes[0]]
        return self.responses[keys[0]]

    @property
    def has_content(self) -> bool:
        resp = self.data_response
        return bool(resp) and resp.has_content

    @property
    def table_name(self) -> str:
        # TODO:
        # 1. Media schema ref name
        # 2. Media schema title property
        # 3. Endpoint title or path component (e.g. first part of path that's not common with all other endpoints)
        name: Optional[str] = None
        if self.data_response:
            if self.list_property:
                name = self.list_property.prop.name
            else:
                name = self.data_response.content_schema.name
        if name:
            return name
        return self.path_table_name

    @property
    def list_property(self) -> Optional[DataPropertyPath]:
        if not self.data_response:
            return None
        return self.data_response.list_property

    @property
    def data_json_path(self) -> str:
        list_prop = self.list_property
        return list_prop.json_path if list_prop else ""

    @property
    def is_transformer(self) -> bool:
        return not not self.required_parameters

    @property
    def transformer(self) -> Optional[TransformerSetting]:
        if not self.parent:
            return None
        if not self.parent.list_property:
            return None
        if not self.path_parameters:
            return None
        if len(self.path_parameters) > 1:
            # TODO: Can't handle endpoints with more than 1 path param for now
            return None
        path_param = list(self.path_parameters.values())[-1]
        list_object = self.parent.list_property.prop
        transformer_arg = list_object.crawled_properties.find_property_by_name(path_param.name, fallback="id")
        if not transformer_arg:
            return None
        return TransformerSetting(
            parent_endpoint=self.parent, parent_property=transformer_arg, path_parameter=path_param
        )

    @classmethod
    def from_operation(
        cls,
        method: TMethod,
        path: str,
        operation: osp.Operation,
        path_table_name: str,
        path_level_parameters: List[Parameter],
        path_summary: Optional[str],
        path_description: Optional[str],
        context: OpenapiContext,
    ) -> "Endpoint":
        # Merge operation params with top level params from path definition
        all_params = {p.name: p for p in path_level_parameters}
        all_params.update(
            {p.name: p for p in (Parameter.from_reference(param, context) for param in operation.parameters or [])}
        )
        responses = {
            status_code: Response.from_reference(status_code, response_ref, context)
            for status_code, response_ref in operation.responses.items()
        }

        operation_id = operation.operationId or f"{method}_{path}"

        credentials = CredentialsProperty.from_requirements(operation.security, context) if operation.security else None

        return cls(
            method=method,
            path=path,
            raw_schema=operation,
            responses=responses,
            parameters=all_params,
            path_table_name=path_table_name,
            operation_id=operation_id,
            python_name=PythonIdentifier(operation_id),
            summary=operation.summary,
            description=operation.description,
            path_summary=path_summary,
            path_description=path_description,
            credentials=credentials,
        )


@dataclass
class EndpointCollection:
    endpoints: List[Endpoint]
    endpoint_tree: Tree
    names_to_render: Optional[Set[str]] = None

    @property
    def all_endpoints_to_render(self) -> List[Endpoint]:
        # return [e for e in self.endpoints if e.has_content]
        return sorted(
            [
                e
                for e in self.endpoints
                if (not self.names_to_render or e.python_name in self.names_to_render) and e.has_content
            ],
            key=lambda e: e.rank,
            reverse=True,
        )

    @property
    def endpoints_by_id(self) -> Dict[str, Endpoint]:
        """Endpoints by operation ID"""
        return {ep.operation_id: ep for ep in self.endpoints}

    @property
    def root_endpoints(self) -> List[Endpoint]:
        return [e for e in self.all_endpoints_to_render if e.list_property and not e.path_parameters]

    @property
    def transformer_endpoints(self) -> List[Endpoint]:
        return [e for e in self.all_endpoints_to_render if e.transformer]

    def set_names_to_render(self, names: Set[str]) -> None:
        self.names_to_render = names

    @classmethod
    def from_context(cls, context: OpenapiContext) -> "EndpointCollection":
        endpoints: list[Endpoint] = []
        all_paths = list(context.spec.paths)
        path_table_names = table_names_from_paths(all_paths)
        for path, path_item in context.spec.paths.items():
            path_level_params = [Parameter.from_reference(param, context) for param in path_item.parameters or []]
            for op_name in context.config.include_methods:
                operation = getattr(path_item, op_name)
                if not operation:
                    continue
                endpoints.append(
                    Endpoint.from_operation(
                        cast(TMethod, op_name),
                        path,
                        operation,
                        path_table_names[path],
                        path_level_params,
                        path_item.summary,
                        path_item.description,
                        context,
                    )
                )
        endpoint_tree = cls.build_endpoint_tree(endpoints)
        result = cls(endpoints=endpoints, endpoint_tree=endpoint_tree)
        process_responses(result)
        for endpoint in result.endpoints:
            endpoint.parent = result.find_nearest_list_parent(endpoint.path)
        for endpoint in result.root_endpoints:
            Pagination.from_endpoint(endpoint)
        return result

    def find_immediate_parent(self, path: str) -> Optional[Endpoint]:
        """Find the parent of the given endpoint.

        Example:
            `find_immediate_parent('/api/v2/ability/{id}') -> Endpoint<'/api/v2/ability'>`
        """
        parts = path.strip("/").split("/")
        while parts:
            current_node = self.endpoint_tree
            parts.pop()
            for part in parts:
                current_node = current_node[part]  # type: ignore
            if "<endpoint>" in current_node:
                return current_node["<endpoint>"]  # type: ignore
        return None

    def find_nearest_list_parent(self, path: str) -> Optional[Endpoint]:
        parts = path.strip("/").split("/")
        while parts:
            current_node = self.endpoint_tree
            parts.pop()
            for part in parts:
                current_node = current_node[part]  # type: ignore[assignment]
            if parent_endpoint := current_node.get("<endpoint>"):
                if cast(Endpoint, parent_endpoint).list_property:
                    return cast(Endpoint, parent_endpoint)
        return None

    @staticmethod
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
