from typing import Optional, Literal, cast

from dataclasses import dataclass

import openapi_schema_pydantic as osp

from parser.context import OpenapiContext

all_operations = ["get", "post", "put", "patch"]  # TODO
TMethod = Literal["get", "post", "put", "patch"]


@dataclass
class Response:
    status_code: str
    raw_schema: osp.Response
    schema: Optional[osp.Schema]

    @classmethod
    def from_reference(
        cls, status_code: str, response_ref: osp.Response | osp.Reference, context: OpenapiContext
    ) -> "Response":
        if isinstance(response_ref, osp.Reference):
            response = context.response_from_reference(response_ref)
        else:
            response = response_ref

        result_schema: Optional[osp.Reference | osp.Schema] = None
        for content_type, media_type in response.content.items():
            # Only json responses
            if content_type == "application/json" or content_type.endswith("+json"):
                result_schema = media_type.media_type_schema
                break

        if isinstance(result_schema, osp.Reference):
            result_schema = context.schema_from_reference(result_schema)

        return cls(status_code=status_code, raw_schema=response, schema=result_schema)


@dataclass
class Endpoint:
    method: TMethod
    responses: dict[str, Response]
    path: str
    raw_schema: osp.Operation

    @classmethod
    def from_operation(
        cls, method: TMethod, path: str, operation: osp.Operation, context: OpenapiContext
    ) -> "Endpoint":
        responses = {
            status_code: Response.from_reference(status_code, response_ref, context)
            for status_code, response_ref in operation.responses.items()
        }
        return cls(method=method, path=path, raw_schema=operation, responses=responses)


class EndpointCollection:
    endpoints: list[Endpoint]

    def __init__(self, context: OpenapiContext) -> None:
        endpoints: list[Endpoint] = []
        for path, path_item in context.spec.paths.items():
            for op_name in all_operations:
                operation = getattr(path_item, op_name)
                if not operation:
                    continue
                endpoints.append(Endpoint.from_operation(cast(TMethod, op_name), path, operation, context))
        self.endpoints = endpoints
