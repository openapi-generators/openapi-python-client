from typing import Optional, List
from dataclasses import dataclass

import openapi_schema_pydantic as osp

from parser.context import OpenapiContext


@dataclass
class OpenApiInfo:
    title: str
    version: str
    summary: Optional[str]
    description: Optional[str]
    # TODO: Servers
    servers: List[osp.Server]

    @classmethod
    def from_context(cls, context: OpenapiContext) -> "OpenApiInfo":
        info = context.spec.info
        title = info.title or context.config.default_openapi_title
        summary = info.summary
        description = info.description
        version = info.version or ""

        return cls(
            title=title, summary=summary, description=description, version=version, servers=context.spec.servers or []
        )
