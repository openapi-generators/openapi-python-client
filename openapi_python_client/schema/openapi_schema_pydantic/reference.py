from typing import Annotated, Any, Literal, TypeVar, Union

from pydantic import BaseModel, ConfigDict, Discriminator, Field, Tag
from typing_extensions import TypeAlias


class Reference(BaseModel):
    """
    A simple object to allow referencing other components in the specification, internally and externally.

    The Reference Object is defined by [JSON Reference](https://tools.ietf.org/html/draft-pbryan-zyp-json-ref-03)
    and follows the same structure, behavior and rules.

    For this specification, reference resolution is accomplished as defined by the JSON Reference specification
    and not by the JSON Schema specification.

    References:
        - https://swagger.io/docs/specification/using-ref/
        - https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#referenceObject
    """

    ref: str = Field(alias="$ref")
    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
        json_schema_extra={
            "examples": [{"$ref": "#/components/schemas/Pet"}, {"$ref": "Pet.json"}, {"$ref": "definitions.json#/Pet"}]
        },
    )


T = TypeVar("T")


def _reference_discriminator(obj: Any) -> Literal["ref", "other"]:
    if isinstance(obj, dict):
        return "ref" if "$ref" in obj else "other"
    return "ref" if isinstance(obj, Reference) else "other"


ReferenceOr: TypeAlias = Annotated[
    Union[Annotated[Reference, Tag("ref")], Annotated[T, Tag("other")]], Discriminator(_reference_discriminator)
]
