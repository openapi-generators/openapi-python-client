from typing import Any

import openapi_schema_pydantic as osp


class OpenapiContext:
    spec: osp.OpenAPI
    schemas: dict[str, Any]

    def response_from_reference(self, ref: osp.Reference) -> osp.Response:
        return self.schemas[ref.ref]

    def schema_from_reference(self, ref: osp.Reference) -> osp.Schema:
        return self.schemas[ref.ref]
