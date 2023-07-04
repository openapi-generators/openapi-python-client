from typing import Dict, Union, cast, Tuple

import openapi_schema_pydantic as osp


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


class OpenapiContext:
    spec: osp.OpenAPI

    _component_cache: Dict[str, Tuple[str, TComponentClass]]

    def __init__(self) -> None:
        self._component_cache = {}

    def _component_from_reference(self, ref: osp.Reference) -> Tuple[str, TComponentClass]:
        url = ref.ref
        if url in self._component_cache:
            return self._component_cache[url]
        if not url.startswith("#/components/"):
            raise ValueError(f"Unsupported ref {url} Only #/components/... refs are supported")
        section, name = url.split("/components/")[-1].split("/")
        obj = getattr(self.spec.components, section)[name]
        self._component_cache[url] = obj
        return name, obj

    def response_from_reference(self, ref: osp.Reference | osp.Response) -> osp.Response:
        if isinstance(ref, osp.Response):
            return ref
        return cast(osp.Response, self._component_from_reference(ref))

    def schema_from_reference(self, ref: osp.Reference | osp.Schema) -> osp.Schema:
        if isinstance(ref, osp.Schema):
            return ref
        return cast(osp.Schema, self._component_from_reference(ref))
