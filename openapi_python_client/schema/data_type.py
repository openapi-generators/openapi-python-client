from enum import Enum


class DataType(str, Enum):
    """The data type of a schema is defined by the type keyword

    References:
        - https://swagger.io/docs/specification/data-models/data-types/
    """

    STRING = "string"
    NUMBER = "number"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    ARRAY = "array"
    OBJECT = "object"
