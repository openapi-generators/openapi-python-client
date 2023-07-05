from typing import Optional, Literal, cast, Union, List

from dataclasses import dataclass

import openapi_schema_pydantic as osp

from parser.context import OpenapiContext
from parser.paths import table_names_from_paths
from parser.models import SchemaWrapper

TMethod = Literal["get", "post", "put", "patch"]


@dataclass
class Parameter:
    name: str
    description: Optional[str]
    schema: SchemaWrapper
    raw_schema: osp.Parameter

    @classmethod
    def from_reference(cls, param_ref: Union[osp.Reference, osp.Parameter], context: OpenapiContext) -> "Parameter":
        osp_param = context.parameter_from_reference(param_ref)
        schema = SchemaWrapper.from_reference(osp_param.param_schema, context)
        description = param_ref.description or osp_param.description or schema.description

        return cls(
            name=osp_param.name,
            description=description,
            raw_schema=osp_param,
            schema=schema,
        )


@dataclass
class Response:
    status_code: str
    description: str
    raw_schema: osp.Response
    content_schema: Optional[SchemaWrapper]

    @classmethod
    def from_reference(
        cls, status_code: str, resp_ref: Union[osp.Reference, osp.Response], context: OpenapiContext
    ) -> "Response":
        raw_schema = context.response_from_reference(resp_ref)
        description = resp_ref.description or raw_schema.description

        content_schema: Optional[SchemaWrapper] = None
        for content_type, media_type in raw_schema.content.items():
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
    parameters: List[Parameter]
    path_table_name: str
    """Table name inferred from path"""
    raw_schema: osp.Operation

    path_summary: Optional[str] = None

    """Summary applying to all methods of the path"""
    path_description: Optional[str] = None
    """Description applying to all methods of the path"""

    @property
    def table_name(self) -> str:
        # 1. Media schema ref name
        # 2. Media schema title property
        # 3. Endpoint title or path component (e.g. first part of path that's not common with all other endpoints)
        raise NotImplementedError("coming soon")

    @classmethod
    def from_operation(
        cls,
        method: TMethod,
        path: str,
        operation: osp.Operation,
        path_table_name: str,
        path_level_parameters: List[Parameter],
        context: OpenapiContext,
    ) -> "Endpoint":
        # Merge operation params with top level params from path definition
        all_params = {p.name: p for p in path_level_parameters}
        all_params.update(
            {p.name: p for p in (Parameter.from_reference(param, context) for param in operation.parameters or [])}
        )
        parameters = list(all_params.values())
        responses = {
            status_code: Response.from_reference(status_code, response_ref, context)
            for status_code, response_ref in operation.responses.items()
        }
        return cls(
            method=method,
            path=path,
            raw_schema=operation,
            responses=responses,
            parameters=parameters,
            path_table_name=path_table_name,
        )


@dataclass
class EndpointCollection:
    endpoints: list[Endpoint]

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
                        cast(TMethod, op_name), path, operation, path_table_names[path], path_level_params, context
                    )
                )
        return EndpointCollection(endpoints=endpoints)
