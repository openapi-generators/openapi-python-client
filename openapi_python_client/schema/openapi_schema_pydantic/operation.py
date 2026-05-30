from pydantic import BaseModel, ConfigDict, Field

from .callback import Callback
from .external_documentation import ExternalDocumentation
from .parameter import Parameter
from .reference import ReferenceOr
from .request_body import RequestBody
from .responses import Responses
from .security_requirement import SecurityRequirement
from .server import Server


class Operation(BaseModel):
    """Describes a single API operation on a path.

    References:
        - https://swagger.io/docs/specification/paths-and-operations/
        - https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#operationObject
    """

    tags: list[str] | None = None
    summary: str | None = None
    description: str | None = None
    externalDocs: ExternalDocumentation | None = None
    operationId: str | None = None
    parameters: list[ReferenceOr[Parameter]] | None = None
    request_body: ReferenceOr[RequestBody] | None = Field(None, alias="requestBody")
    responses: Responses
    callbacks: dict[str, Callback] | None = None

    deprecated: bool = False
    security: list[SecurityRequirement] | None = None
    servers: list[Server] | None = None
    model_config = ConfigDict(
        # `Callback` contains an unresolvable forward reference, will rebuild in `__init__.py`:
        defer_build=True,
        extra="allow",
        json_schema_extra={
            "examples": [
                {
                    "tags": ["pet"],
                    "summary": "Updates a pet in the store with form data",
                    "operationId": "updatePetWithForm",
                    "parameters": [
                        {
                            "name": "petId",
                            "in": "path",
                            "description": "ID of pet that needs to be updated",
                            "required": True,
                            "schema": {"type": "string"},
                        }
                    ],
                    "requestBody": {
                        "content": {
                            "application/x-www-form-urlencoded": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "name": {
                                            "description": "Updated name of the pet",
                                            "type": "string",
                                        },
                                        "status": {
                                            "description": "Updated status of the pet",
                                            "type": "string",
                                        },
                                    },
                                    "required": ["status"],
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Pet updated.",
                            "content": {"application/json": {}, "application/xml": {}},
                        },
                        "405": {
                            "description": "Method Not Allowed",
                            "content": {"application/json": {}, "application/xml": {}},
                        },
                    },
                    "security": [{"petstore_auth": ["write:pets", "read:pets"]}],
                }
            ]
        },
    )
