from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..untrusted_string import UntrustedString
from .example import Example
from .media_type import MediaType
from .reference import ReferenceOr
from .schema import Schema


class Header(BaseModel):
    """
    The Header Object follows the structure of the [Parameter Object](#parameterObject) with the following changes:

    1. `name` MUST NOT be specified, it is given in the corresponding `headers` map.
    2. `in` MUST NOT be specified, it is implicitly in `header`.
    3. All traits that are affected by the location MUST be applicable to a location of `header`
       (for example, [`style`](#parameterStyle)).

    References:
        - https://swagger.io/docs/specification/describing-parameters/#header-parameters
        - https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#headerObject
    """

    description: UntrustedString | None = None
    required: bool = False
    deprecated: bool = False
    allowEmptyValue: bool = False
    style: UntrustedString | None = None
    explode: bool = False
    allowReserved: bool = False
    param_schema: ReferenceOr[Schema] | None = Field(default=None, alias="schema")
    example: Any | None = None
    examples: dict[UntrustedString, ReferenceOr[Example]] | None = None
    content: dict[UntrustedString, MediaType] | None = None
    model_config = ConfigDict(
        # `Parameter` is not build yet, will rebuild in `__init__.py`:
        defer_build=True,
        extra="allow",
        populate_by_name=True,
        json_schema_extra={
            "examples": [
                {"description": "The number of allowed requests in the current period", "schema": {"type": "integer"}}
            ]
        },
    )
