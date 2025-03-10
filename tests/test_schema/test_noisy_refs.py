# If a field may be reference (`Union[Reference, OtherType]`) and the dictionary
# being processed for it contains "$ref", it seems like it should preferentially
# be parsed as a `Reference`[1].  Since the models are defined with
# `extra="allow"`, Pydantic won't guarantee this parse if the dictionary is in
# an unspecified sense a "better match" for `OtherType`[2], e.g., perhaps if it
# has several more fields matching that type versus the single match for `$ref`.
#
# We can use a discriminated union to force parsing these dictionaries as
# `Reference`s.
#
# References:
#   [1] https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#reference-object
#   [2] https://docs.pydantic.dev/latest/concepts/unions/#smart-mode
import json
from typing import Annotated, TypeVar, Union, get_args, get_origin

import pytest
from pydantic import TypeAdapter

from openapi_python_client.schema.openapi_schema_pydantic import (
    Callback,
    Example,
    Header,
    Link,
    Parameter,
    PathItem,
    Reference,
    RequestBody,
    Response,
    Schema,
    SecurityScheme,
)

try:
    from openapi_python_client.schema.openapi_schema_pydantic.reference import ReferenceOr
except ImportError:
    T = TypeVar("T")
    ReferenceOr = Union[Reference, T]


def get_example(base_type):
    schema = base_type.model_json_schema()
    print(json.dumps(schema.get("examples", []), indent=4))
    if "examples" in schema:
        return schema["examples"][0]
    if "$defs" in schema:
        return schema["$defs"][base_type.__name__]["examples"][0]
    raise TypeError(f"No example found for {base_type.__name__}")


def deannotate_type(t):
    while get_origin(t) is Annotated:
        t = get_args(t)[0]
    return t


# The following types occur in various models, so we want to make sure they
# parse properly.  They are verified to /fail/ to parse as of commit 3bd12f86.

@pytest.mark.parametrize(("ref_or_type", "get_example_fn"), [
    (ReferenceOr[Callback], lambda t: {"test1": get_example(PathItem),
                                       "test2": get_example(PathItem)}),
    (ReferenceOr[Example], get_example),
    (ReferenceOr[Header], get_example),
    (ReferenceOr[Link], get_example),
    (ReferenceOr[Parameter], get_example),
    (ReferenceOr[RequestBody], get_example),
    (ReferenceOr[Response], get_example),
    (ReferenceOr[Schema], get_example),
    (ReferenceOr[SecurityScheme], get_example),
])
def test_type(ref_or_type, get_example_fn):
    base_type = None
    print(deannotate_type(ref_or_type))
    for maybe_annotated_type in get_args(deannotate_type(ref_or_type)):
        each_type = deannotate_type(maybe_annotated_type)
        if each_type is not Reference:
            base_type = each_type
            break
    assert base_type is not None

    example = get_example_fn(base_type)

    parsed = TypeAdapter(ref_or_type).validate_python(example)
    assert type(parsed) is get_origin(base_type) or base_type

    example["$ref"] = "ref"
    parsed = TypeAdapter(ref_or_type).validate_python(example)
    assert type(parsed) is Reference
