from typing import List, Optional

from pydantic import BaseModel

from .components import Components
from .external_documentation import ExternalDocumentation
from .info import Info
from .paths import Paths
from .security_requirement import SecurityRequirement
from .server import Server
from .tag import Tag


class OpenAPI(BaseModel):
    """This is the root document object of the OpenAPI document."""

    info: Info
    """
    **REQUIRED**. Provides metadata about the API. The metadata MAY be used by tooling as required.
    """

    servers: List[Server] = [Server(url="/")]
    """
    An array of Server Objects, which provide connectivity information to a target server.
    If the `servers` property is not provided, or is an empty array,
    the default value would be a [Server Object](#serverObject) with a [url](#serverUrl) value of `/`.
    """

    paths: Paths
    """
    **REQUIRED**. The available paths and operations for the API.
    """

    components: Optional[Components] = None
    """
    An element to hold various schemas for the specification.
    """

    security: Optional[List[SecurityRequirement]] = None
    """
    A declaration of which security mechanisms can be used across the API.
    The list of values includes alternative security requirement objects that can be used.
    Only one of the security requirement objects need to be satisfied to authorize a request.
    Individual operations can override this definition.
    To make security optional, an empty security requirement (`{}`) can be included in the array.
    """

    tags: Optional[List[Tag]] = None
    """
    A list of tags used by the specification with additional metadata.
    The order of the tags can be used to reflect on their order by the parsing tools.
    Not all tags that are used by the [Operation Object](#operationObject) must be declared.
    The tags that are not declared MAY be organized randomly or based on the tools' logic.
    Each tag name in the list MUST be unique.
    """

    externalDocs: Optional[ExternalDocumentation] = None
    """
    Additional external documentation.
    """
