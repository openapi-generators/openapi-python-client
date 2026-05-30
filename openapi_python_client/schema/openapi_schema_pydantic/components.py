from pydantic import BaseModel, ConfigDict

from .callback import Callback
from .example import Example
from .header import Header
from .link import Link
from .parameter import Parameter
from .reference import ReferenceOr
from .request_body import RequestBody
from .response import Response
from .schema import Schema
from .security_scheme import SecurityScheme


class Components(BaseModel):
    """
    Holds a set of reusable objects for different aspects of the OAS.
    All objects defined within the components object will have no effect on the API
    unless they are explicitly referenced from properties outside the components object.

    References:
        - https://swagger.io/docs/specification/components/
        - https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#componentsObject
    """

    schemas: dict[str, ReferenceOr[Schema]] | None = None
    responses: dict[str, ReferenceOr[Response]] | None = None
    parameters: dict[str, ReferenceOr[Parameter]] | None = None
    examples: dict[str, ReferenceOr[Example]] | None = None
    requestBodies: dict[str, ReferenceOr[RequestBody]] | None = None
    headers: dict[str, ReferenceOr[Header]] | None = None
    securitySchemes: dict[str, ReferenceOr[SecurityScheme]] | None = None
    links: dict[str, ReferenceOr[Link]] | None = None
    callbacks: dict[str, ReferenceOr[Callback]] | None = None
    model_config = ConfigDict(
        # `Callback` contains an unresolvable forward reference, will rebuild in `__init__.py`:
        defer_build=True,
        extra="allow",
        json_schema_extra={
            "examples": [
                {
                    "schemas": {
                        "GeneralError": {
                            "type": "object",
                            "properties": {
                                "code": {"type": "integer", "format": "int32"},
                                "message": {"type": "string"},
                            },
                        },
                        "Category": {
                            "type": "object",
                            "properties": {"id": {"type": "integer", "format": "int64"}, "name": {"type": "string"}},
                        },
                        "Tag": {
                            "type": "object",
                            "properties": {"id": {"type": "integer", "format": "int64"}, "name": {"type": "string"}},
                        },
                    },
                    "parameters": {
                        "skipParam": {
                            "name": "skip",
                            "in": "query",
                            "description": "number of items to skip",
                            "required": True,
                            "schema": {"type": "integer", "format": "int32"},
                        },
                        "limitParam": {
                            "name": "limit",
                            "in": "query",
                            "description": "max records to return",
                            "required": True,
                            "schema": {"type": "integer", "format": "int32"},
                        },
                    },
                    "responses": {
                        "NotFound": {"description": "Entity not found."},
                        "IllegalInput": {"description": "Illegal input for operation."},
                        "GeneralError": {
                            "description": "General Error",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/GeneralError"}}},
                        },
                    },
                    "securitySchemes": {
                        "api_key": {"type": "apiKey", "name": "api_key", "in": "header"},
                        "petstore_auth": {
                            "type": "oauth2",
                            "flows": {
                                "implicit": {
                                    "authorizationUrl": "http://example.org/api/oauth/dialog",
                                    "scopes": {
                                        "write:pets": "modify pets in your account",
                                        "read:pets": "read your pets",
                                    },
                                }
                            },
                        },
                    },
                }
            ]
        },
    )
