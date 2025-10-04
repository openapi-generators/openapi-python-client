from enum import Enum


class Style(str, Enum):
    """The style of a schema is defined by the style keyword

    References:
        - https://swagger.io/docs/specification/v3_0/serialization/
        - https://spec.openapis.org/oas/latest.html#fixed-fields-for-use-with-schema
    """

    SIMPLE = "simple"
    LABEL = "label"
    MATRIX = "matrix"
    FORM = "form"
    SPACE_DELIMITED = "spaceDelimited"
    PIPE_DELIMITED = "pipeDelimited"
    DEEP_OBJECT = "deepObject"
