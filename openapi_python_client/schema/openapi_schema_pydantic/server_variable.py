from typing import List, Optional

from pydantic import BaseModel, Extra


class ServerVariable(BaseModel):
    """An object representing a Server Variable for server URL template substitution.

    References:
        - https://swagger.io/docs/specification/api-host-and-base-path/
        - https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#serverVariableObject
    """

    enum: Optional[List[str]] = None
    default: str
    description: Optional[str] = None

    class Config:  # pylint: disable=missing-class-docstring
        extra = Extra.allow
