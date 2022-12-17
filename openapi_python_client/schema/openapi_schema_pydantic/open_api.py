# pylint: disable=W0611
import sys
from typing import List, Optional, Union

from pydantic import BaseModel, Extra

from .components import Components
from .external_documentation import ExternalDocumentation
from .info import Info
from .paths import Paths
from .security_requirement import SecurityRequirement
from .server import Server
from .tag import Tag

if sys.version_info.minor < 8:
    from typing_extensions import Literal
else:
    from typing import Literal  # type: ignore


class OpenAPI(BaseModel):
    """This is the root document object of the OpenAPI document.

    References:
        - https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#oasObject
        - https://swagger.io/docs/specification/basic-structure/
    """

    info: Info
    servers: List[Server] = [Server(url="/")]
    paths: Paths
    components: Optional[Components] = None
    security: Optional[List[SecurityRequirement]] = None
    tags: Optional[List[Tag]] = None
    externalDocs: Optional[ExternalDocumentation] = None
    openapi: 'Union[Literal["3.0.0"], Literal["3.0.1"], Literal["3.0.2"], Literal["3.0.3"]]'

    class Config:  # pylint: disable=missing-class-docstring
        extra = Extra.allow
