from typing import Dict, Any, Union, Type, Literal, Tuple

import openapi_schema_pydantic as osp

import jsonschema

TComponentSection = Literal[
    "schemas", "parameters", "responses", "headers", "examples", "links", "securitySchemes", "requestBodies"
]

TComponentClass = Union[
    osp.Schema,
    osp.Parameter,
    osp.Response,
    osp.Header,
    osp.Example,
    osp.Link,
    osp.SecurityScheme,
    osp.RequestBody,
]


class RefResolver:
    component_types: Dict[TComponentSection, Type[TComponentClass]] = {
        "schemas": osp.Schema,
        "parameters": osp.Parameter,
        "responses": osp.Response,
        "headers": osp.Header,
        "examples": osp.Example,
        "links": osp.Link,
        "securitySchemes": osp.SecurityScheme,
        "requestBodies": osp.RequestBody,
    }

    def __init__(self, spec: Dict[str, Any]) -> None:
        self._resolver = jsonschema.RefResolver("", spec)

    def resolve(self, ref: str) -> TComponentClass:
        _, schema = self._resolver.resolve(ref)

        section: TComponentSection = ref.split("/components/")[-1].split("/")[0]  # type: ignore[assignment]
        klass = self.component_types[section]

        return klass.parse_obj(schema)
