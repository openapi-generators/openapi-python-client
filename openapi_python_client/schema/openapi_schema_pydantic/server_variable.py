from pydantic import BaseModel, ConfigDict

from ..untrusted_string import UntrustedString


class ServerVariable(BaseModel):
    """An object representing a Server Variable for server URL template substitution.

    References:
        - https://swagger.io/docs/specification/api-host-and-base-path/
        - https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#serverVariableObject
    """

    enum: list[UntrustedString] | None = None
    default: UntrustedString
    description: UntrustedString | None = None
    model_config = ConfigDict(extra="allow")
