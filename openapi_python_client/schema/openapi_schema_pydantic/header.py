from pydantic import Extra, Field

from ..parameter_location import ParameterLocation
from .parameter import Parameter


class Header(Parameter):
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

    name = Field(default="", const=True)
    param_in = Field(default=ParameterLocation.HEADER, const=True, alias="in")

    class Config:  # pylint: disable=missing-class-docstring
        extra = Extra.allow
        allow_population_by_field_name = True
        schema_extra = {
            "examples": [
                {"description": "The number of allowed requests in the current period", "schema": {"type": "integer"}}
            ]
        }
