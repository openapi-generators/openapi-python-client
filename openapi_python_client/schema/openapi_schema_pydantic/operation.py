from typing import List, Optional, Union

from pydantic import BaseModel

from .external_documentation import ExternalDocumentation
from .parameter import Parameter
from .reference import Reference
from .request_body import RequestBody
from .responses import Responses
from .security_requirement import SecurityRequirement
from .server import Server


class Operation(BaseModel):
    """Describes a single API operation on a path."""

    tags: Optional[List[str]] = None
    """
    A list of tags for API documentation control.
    Tags can be used for logical grouping of operations by resources or any other qualifier.
    """

    summary: Optional[str] = None
    """
    A short summary of what the operation does.
    """

    description: Optional[str] = None
    """
    A verbose explanation of the operation behavior.
    [CommonMark syntax](https://spec.commonmark.org/) MAY be used for rich text representation.
    """

    externalDocs: Optional[ExternalDocumentation] = None
    """
    Additional external documentation for this operation.
    """

    operationId: Optional[str] = None
    """
    Unique string used to identify the operation.
    The id MUST be unique among all operations described in the API.
    The operationId value is **case-sensitive**.
    Tools and libraries MAY use the operationId to uniquely identify an operation,
    therefore, it is RECOMMENDED to follow common programming naming conventions.
    """

    parameters: Optional[List[Union[Parameter, Reference]]] = None
    """
    A list of parameters that are applicable for this operation.
    If a parameter is already defined at the [Path Item](#pathItemParameters),
    the new definition will override it but can never remove it.
    The list MUST NOT include duplicated parameters.
    A unique parameter is defined by a combination of a [name](#parameterName) and [location](#parameterIn).
    The list can use the [Reference Object](#referenceObject) to link to parameters
    that are defined at the [OpenAPI Object's components/parameters](#componentsParameters).
    """

    requestBody: Optional[Union[RequestBody, Reference]] = None
    """
    The request body applicable for this operation.

    The `requestBody` is only supported in HTTP methods where the HTTP 1.1 specification
    [RFC7231](https://tools.ietf.org/html/rfc7231#section-4.3.1) has explicitly defined semantics for request bodies.
    In other cases where the HTTP spec is vague, `requestBody` SHALL be ignored by consumers.
    """

    responses: Responses
    """
    **REQUIRED**. The list of possible responses as they are returned from executing this operation.
    """

    deprecated: bool = False
    """
    Declares this operation to be deprecated.
    Consumers SHOULD refrain from usage of the declared operation.
    Default value is `false`.
    """

    security: Optional[List[SecurityRequirement]] = None
    """
    A declaration of which security mechanisms can be used for this operation.
    The list of values includes alternative security requirement objects that can be used.
    Only one of the security requirement objects need to be satisfied to authorize a request.
    To make security optional, an empty security requirement (`{}`) can be included in the array.
    This definition overrides any declared top-level [`security`](#oasSecurity).
    To remove a top-level security declaration, an empty array can be used.
    """

    servers: Optional[List[Server]] = None
    """
    An alternative `server` array to service this operation.
    If an alternative `server` object is specified at the Path Item Object or Root level,
    it will be overridden by this value.
    """

    class Config:
        schema_extra = {
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
                                        "name": {"description": "Updated name of the pet", "type": "string"},
                                        "status": {"description": "Updated status of the pet", "type": "string"},
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
        }
