from typing import Optional, Literal, cast, Union

from dataclasses import dataclass

import openapi_schema_pydantic as osp

from parser.context import OpenapiContext
from parser.models import Response

all_operations = ["get", "post", "put", "patch"]  # TODO
TMethod = Literal["get", "post", "put", "patch"]


# @dataclass
# class Response:
#     status_code: str
#     raw_schema: osp.Response
#     body_schema: Optional[osp.Schema]

#     @classmethod
#     def from_reference(
#         cls, status_code: str, response_ref: osp.Response | osp.Reference, context: OpenapiContext
#     ) -> "Response":
#         response = context.response_from_reference(response_ref)

#         result_schema: Optional[osp.Reference | osp.Schema] = None
#         for content_type, media_type in response.content.items():
#             # Only json responses
#             if content_type == "application/json" or content_type.endswith("+json"):
#                 result_schema = media_type.media_type_schema
#                 break

#         body_schema = context.schema_from_reference(result_schema)

#         return cls(status_code=status_code, raw_schema=response, body_schema=body_schema)


def build_response(status_code: str, resp_ref: Union[osp.Reference, osp.Response], context: OpenapiContext) -> Response:
    osp_response = context.response_from_reference(resp_ref)
    media_schema: Optional[Union[osp.Reference | osp.Schema]] = None
    for content_type, media_type in osp_response.content.items():
        if content_type == "application/json" or content_type.endswith("+json"):
            media_schema = media_type.media_type_schema
            break

    media_schema = context.schema_from_reference(media_schema) if media_schema else None
    return Response(osp_response, media_schema, status_code, resp_ref.description or osp_response.description)


@dataclass
class Endpoint:
    method: TMethod
    responses: dict[str, Response]
    path: str
    raw_schema: osp.Operation

    @property
    def table_name(self) -> str:
        # 1. Media schema ref name
        # 2. Media schema title property
        # 3. Endpoint title or path component (e.g. first part of path that's not common with all other endpoints)
        raise NotImplementedError("coming soon")

    @classmethod
    def from_operation(
        cls, method: TMethod, path: str, operation: osp.Operation, context: OpenapiContext
    ) -> "Endpoint":
        responses = {
            status_code: Response.from_reference(status_code, response_ref, context)
            for status_code, response_ref in operation.responses.items()
        }
        return cls(method=method, path=path, raw_schema=operation, responses=responses)


@dataclass
class EndpointCollection:
    endpoints: list[Endpoint]

    @classmethod
    def from_context(cls, context: OpenapiContext) -> "EndpointCollection":
        endpoints: list[Endpoint] = []
        for path, path_item in context.spec.paths.items():
            for op_name in all_operations:
                operation = getattr(path_item, op_name)
                if not operation:
                    continue
                endpoints.append(Endpoint.from_operation(cast(TMethod, op_name), path, operation, context))
        return EndpointCollection(endpoints=endpoints)
