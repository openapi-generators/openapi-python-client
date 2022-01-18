from typing import List, Optional, Union

from pydantic import BaseModel, Extra, Field

from .operation import Operation
from .parameter import Parameter
from .reference import Reference
from .server import Server


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

    ref: Optional[str] = Field(default=None, alias="$ref")
    summary: Optional[str] = None
    description: Optional[str] = None
    get: Optional[Operation] = None
    put: Optional[Operation] = None
    post: Optional[Operation] = None
    delete: Optional[Operation] = None
    options: Optional[Operation] = None
    head: Optional[Operation] = None
    patch: Optional[Operation] = None
    trace: Optional[Operation] = None
    servers: Optional[List[Server]] = None
    parameters: Optional[List[Union[Parameter, Reference]]] = None

    class Config:  # pylint: disable=missing-class-docstring
        extra = Extra.allow
        allow_population_by_field_name = True
        schema_extra = {
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
        }
