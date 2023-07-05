from typing import Dict, Union, cast, Tuple, Optional

import openapi_schema_pydantic as osp

from parser.config import Config


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

    _component_cache: Dict[str, TComponentClass]

    def __init__(self, config: Config) -> None:
        self.config = config
        self._component_cache = {}

    def _component_from_reference(self, ref: osp.Reference) -> TComponentClass:
        url = ref.ref
        if url in self._component_cache:
            return self._component_cache[url]
        if not url.startswith("#/components/"):
            raise ValueError(f"Unsupported ref {url} Only #/components/... refs are supported")
        section, name = url.split("/components/")[-1].split("/")
        obj = getattr(self.spec.components, section)[name]
        self._component_cache[url] = obj
        return obj

    def schema_and_name_from_reference(self, ref: Union[osp.Reference, osp.Schema]) -> Tuple[str, osp.Schema]:
        name: Optional[str] = None
        if isinstance(ref, osp.Response):
            name = ref.ref.split("/components/")[-1].split("/")[-1]
        schema = self.schema_from_reference(ref)
        name = name or schema.title
        return name, schema

    def response_from_reference(self, ref: osp.Reference | osp.Response) -> osp.Response:
        if isinstance(ref, osp.Response):
            return ref
        return cast(osp.Response, self._component_from_reference(ref))

    def schema_from_reference(self, ref: osp.Reference | osp.Schema) -> osp.Schema:
        if isinstance(ref, osp.Schema):
            return ref
        return cast(osp.Schema, self._component_from_reference(ref))

    def parameter_from_reference(self, ref: Union[osp.Reference, osp.Parameter]) -> osp.Parameter:
        if isinstance(ref, osp.Parameter):
            return ref
        return cast(osp.Parameter, self._component_from_reference(ref))
