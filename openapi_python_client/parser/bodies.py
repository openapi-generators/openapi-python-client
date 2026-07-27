from collections.abc import Iterator
from enum import StrEnum
from typing import Any

import attr

from openapi_python_client.parser.properties import (
    ModelProperty,
    Property,
    Schemas,
    property_from_data,
)
from openapi_python_client.parser.properties.schemas import get_reference_simple_name

from .. import schema as oai
from ..config import Config
from ..utils import get_content_type
from .errors import ErrorLevel, ParseError

MULTIPART_CONTENT_TYPE = "multipart/form-data"
_OCTET_STREAM = "application/octet-stream"
_SCHEMAS_REF_PREFIX = "#/components/schemas/"


class BodyType(StrEnum):
    JSON = "json"
    DATA = "data"
    FILES = "files"
    CONTENT = "content"


@attr.define
class Body:
    content_type: str
    prop: Property
    body_type: BodyType


def body_from_data(
    *,
    data: oai.Operation,
    schemas: Schemas,
    request_bodies: dict[str, oai.RequestBody | oai.Reference],
    config: Config,
    endpoint_name: str,
) -> tuple[list[Body | ParseError], Schemas]:
    """Adds form or JSON body to Endpoint if included in data"""
    body = _resolve_reference(data.request_body, request_bodies)
    if isinstance(body, ParseError):
        return [body], schemas
    if body is None:
        return [], schemas

    bodies: list[Body | ParseError] = []
    body_content = body.content
    prefix_type_names = len(body_content) > 1

    for content_type, media_type in body_content.items():
        simplified_content_type = get_content_type(content_type, config)
        if simplified_content_type is None:
            bodies.append(
                ParseError(
                    detail="Invalid content type",
                    data=body,
                    level=ErrorLevel.WARNING,
                )
            )
            continue
        media_type_schema = media_type.media_type_schema
        if media_type_schema is None:
            bodies.append(
                ParseError(
                    detail="Missing schema",
                    data=body,
                    level=ErrorLevel.WARNING,
                )
            )
            continue
        if simplified_content_type == "application/x-www-form-urlencoded":
            body_type = BodyType.DATA
        elif simplified_content_type == MULTIPART_CONTENT_TYPE:
            body_type = BodyType.FILES
        elif simplified_content_type == "application/octet-stream":
            body_type = BodyType.CONTENT
        elif simplified_content_type == "application/json" or simplified_content_type.endswith("+json"):
            body_type = BodyType.JSON
        else:
            bodies.append(
                ParseError(
                    detail=f"Unsupported content type {simplified_content_type}",
                    data=body,
                    level=ErrorLevel.WARNING,
                )
            )
            continue
        prop, schemas = property_from_data(
            name="body",
            required=body.required,
            data=media_type_schema,
            schemas=schemas,
            parent_name=f"{endpoint_name}_{body_type}" if prefix_type_names else endpoint_name,
            config=config,
        )
        if isinstance(prop, ParseError):
            bodies.append(prop)
            continue
        if isinstance(prop, ModelProperty) and body_type == BodyType.FILES:
            # Regardless of if we just made this property or found it, it now needs the `to_multipart` method
            prop = attr.evolve(prop, is_multipart_body=True)
            schemas = attr.evolve(
                schemas,
                classes_by_name={
                    **schemas.classes_by_name,
                    prop.class_info.name: prop,
                },
                models_to_process=[*schemas.models_to_process, prop],
            )
        bodies.append(
            Body(
                content_type=content_type,
                prop=prop,
                body_type=body_type,
            )
        )

    return bodies, schemas


def _resolve_reference(
    body: oai.RequestBody | oai.Reference | None, request_bodies: dict[str, oai.RequestBody | oai.Reference]
) -> oai.RequestBody | ParseError | None:
    if body is None:
        return None
    references_seen = []
    while isinstance(body, oai.Reference) and body.ref not in references_seen:
        references_seen.append(body.ref)
        body = request_bodies.get(get_reference_simple_name(body.ref))
    if isinstance(body, oai.Reference):
        return ParseError(detail="Circular $ref in request body", data=body)
    if body is None and references_seen:
        return ParseError(detail=f"Could not resolve $ref {references_seen[-1]} in request body")
    return body


def mark_multipart_file_properties(document: dict[str, Any]) -> None:
    """Annotate ``multipart/form-data`` file parts with ``format: binary``, in place.

    OpenAPI 3.0 spells a file part ``{"type": "string", "format": "binary"}``. OpenAPI
    3.1 dropped that meaning of ``format`` and spells it
    ``{"type": "string", "contentMediaType": "application/octet-stream"}`` instead --
    which is what FastAPI emits for every ``UploadFile``. Only ``format`` reaches
    ``FileProperty``, so without this pass a 3.1 upload is generated as a plain ``str``
    and sent as a nameless ``text/plain`` part that the server rejects.

    The two spellings cannot be unified by looking at a property on its own: FastAPI
    gives a ``bytes`` field on a *JSON* body the byte-for-byte identical schema, and
    there the value really is transported as a string. So the rule is applied only to
    schemas reached through a ``multipart/form-data`` body, where
    ``application/octet-stream`` can only mean a file.

    A schema referenced by both a multipart body and any other media type is left alone
    rather than guessed at -- annotating a shared component would change how it is
    generated everywhere it is used.
    """
    if not isinstance(document, dict):
        # An unparseable document still has to reach model_validate, which is what
        # turns it into a readable "Failed to parse OpenAPI document" error.
        return

    components = document.get("components")
    component_schemas = components.get("schemas") if isinstance(components, dict) else None
    if not isinstance(component_schemas, dict):
        component_schemas = {}

    multipart_refs: set[str] = set()
    other_refs: set[str] = set()
    targets: list[dict[str, Any]] = []

    for content_type, media_type in _iter_media_types(document):
        schema = media_type.get("schema")
        if not isinstance(schema, dict):
            continue
        is_multipart = content_type.split(";")[0].strip().lower() == MULTIPART_CONTENT_TYPE
        ref = schema.get("$ref")
        if isinstance(ref, str):
            (multipart_refs if is_multipart else other_refs).add(ref)
        elif is_multipart:
            targets.append(schema)

    for ref in sorted(multipart_refs - other_refs):
        if not ref.startswith(_SCHEMAS_REF_PREFIX):
            continue
        resolved = component_schemas.get(ref[len(_SCHEMAS_REF_PREFIX) :])
        if isinstance(resolved, dict):
            targets.append(resolved)

    for target in targets:
        _mark_binary_properties(target)


def _iter_media_types(node: Any) -> Iterator[tuple[str, dict[str, Any]]]:
    """Yield every ``(content type, media type object)`` pair anywhere in the document.

    Walking the whole document rather than the known locations of a ``content`` map
    keeps request bodies, responses, ``components``, and content-typed parameters all
    covered. A schema property that happens to be named ``content`` cannot be mistaken
    for a content map: its keys are schema keywords, none of which contain a ``/``.
    """
    if isinstance(node, dict):
        content = node.get("content")
        if isinstance(content, dict):
            for content_type, media_type in content.items():
                if isinstance(content_type, str) and "/" in content_type and isinstance(media_type, dict):
                    yield content_type, media_type
        for value in node.values():
            yield from _iter_media_types(value)
    elif isinstance(node, list):
        for item in node:
            yield from _iter_media_types(item)


def _mark_binary_properties(schema: dict[str, Any]) -> None:
    """Annotate the direct properties of one multipart body schema.

    Only the body's own properties are visited. Nested objects are not multipart parts
    -- each part is a top-level form field -- and following a property-level ``$ref``
    would reach a component that other schemas may share.
    """
    for subschema in schema.get("allOf") or []:
        if isinstance(subschema, dict) and "$ref" not in subschema:
            _mark_binary_properties(subschema)

    properties = schema.get("properties")
    if not isinstance(properties, dict):
        return
    for property_schema in properties.values():
        if isinstance(property_schema, dict):
            _mark_binary_string(property_schema)


def _mark_binary_string(schema: dict[str, Any]) -> None:
    """Add ``format: binary`` to a schema describing binary content, or to its members.

    Handles the three shapes FastAPI produces for a part: ``UploadFile``,
    ``list[UploadFile]``, and ``UploadFile | None`` (an ``anyOf`` against ``null``).
    """
    if _is_binary_string(schema):
        schema.setdefault("format", "binary")
        return

    items = schema.get("items")
    if isinstance(items, dict) and _is_binary_string(items):
        items.setdefault("format", "binary")

    for key in ("anyOf", "oneOf"):
        for member in schema.get(key) or []:
            if isinstance(member, dict) and _is_binary_string(member):
                member.setdefault("format", "binary")


def _is_binary_string(schema: dict[str, Any]) -> bool:
    if schema.get("contentMediaType") != _OCTET_STREAM:
        return False
    schema_type = schema.get("type")
    return schema_type == "string" or (isinstance(schema_type, list) and "string" in schema_type)
