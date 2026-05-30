from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

from .parameter import Parameter
from .reference import ReferenceOr
from .server import Server

if TYPE_CHECKING:
    from .operation import Operation  # pragma: no cover


class PathItem(BaseModel):
    """
    Describes the operations available on a single path.
    A Path Item MAY be empty, due to [ACL constraints](#securityFiltering).
    The path itself is still exposed to the documentation viewer
    but they will not know which operations and parameters are available.

    References:
        - https://swagger.io/docs/specification/paths-and-operations/
        - https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#pathItemObject
    """

    ref: str | None = Field(default=None, alias="$ref")
    summary: str | None = None
    description: str | None = None
    get: "Operation | None" = None
    put: "Operation | None" = None
    post: "Operation | None" = None
    delete: "Operation | None" = None
    options: "Operation | None" = None
    head: "Operation | None" = None
    patch: "Operation | None" = None
    trace: "Operation | None" = None
    servers: list[Server] | None = None
    parameters: list[ReferenceOr[Parameter]] | None = None
    model_config = ConfigDict(
        # `Operation` is an unresolvable forward reference, will rebuild in `__init__.py`:
        defer_build=True,
        extra="allow",
        populate_by_name=True,
        json_schema_extra={
            "examples": [
                {
                    "get": {
                        "description": "Returns pets based on ID",
                        "summary": "Find pets by ID",
                        "operationId": "getPetsById",
                        "responses": {
                            "200": {
                                "description": "pet response",
                                "content": {
                                    "*/*": {"schema": {"type": "array", "items": {"$ref": "#/components/schemas/Pet"}}}
                                },
                            },
                            "default": {
                                "description": "error payload",
                                "content": {"text/html": {"schema": {"$ref": "#/components/schemas/ErrorModel"}}},
                            },
                        },
                    },
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "description": "ID of pet to use",
                            "required": True,
                            "schema": {"type": "array", "items": {"type": "string"}},
                            "style": "simple",
                        }
                    ],
                }
            ]
        },
    )
