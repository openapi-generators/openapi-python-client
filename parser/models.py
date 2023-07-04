from typing import Literal, TYPE_CHECKING, Optional

from dataclasses import dataclass

import openapi_schema_pydantic as osp

if TYPE_CHECKING:
    from parser.context import OpenapiContext


TSchemaType = Literal["null", "boolean", "object", "array", "number", "string", "integer"]


@dataclass
class Schema:
    schema: osp.Schema
    name: str
    type: TSchemaType


@dataclass
class Response:
    schema: osp.Response
    root_object: Schema | None
    status_code: str
    description: str


@dataclass
class Parameter:
    schema: osp.Parameter
    param_schema: Schema | None
    description: str | None
    """Description of param for docstring. May come from ref or the param_schema"""

    @classmethod
    def from_reference(
        cls, status_code: str, response_ref: osp.Response | osp.Reference, context: OpenapiContext
    ) -> "Response":
        pass
