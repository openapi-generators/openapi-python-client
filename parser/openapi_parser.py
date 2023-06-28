import json
import mimetypes
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterator, Optional, Union
import httpcore

import httpx
import jsonschema
import openapi_schema_pydantic
import yaml

from parser.context import OpenapiContext


class OpenapiParser:
    spec_raw: Dict[str, Any]

    def __init__(self, spec_file: Path) -> None:
        self.spec_file = spec_file
        self.context = OpenapiContext()

    def load_spec_raw(self) -> Dict[str, Any]:
        return _get_document(path=self.spec_file)

    def _find_references(self, dictionary: Dict[str, Any]) -> Iterator[str]:
        if isinstance(dictionary, dict):
            if "$ref" in dictionary and isinstance(dictionary["$ref"], str):
                yield dictionary["$ref"]
            else:
                for key, value in dictionary.items():
                    yield from self._find_references(value)
        elif isinstance(dictionary, list):
            for item in dictionary:
                yield from self._find_references(item)

    def parse(self) -> None:
        self.spec_raw = self.load_spec_raw()
        reference_urls = set(self._find_references(self.spec_raw))

        resolver = jsonschema.RefResolver("", self.spec_raw)
        resolved_refs = {}
        for url in reference_urls:
            key, schema = resolver.resolve(url)
            resolved_refs[key] = openapi_schema_pydantic.Schema.parse_obj(schema)
        self.context.schemas = resolved_refs
        self.context.spec = openapi_schema_pydantic.OpenAPI.parse_obj(self.spec_raw)


def _load_yaml_or_json(data: bytes, content_type: Optional[str]) -> Dict[str, Any]:
    if content_type == "application/json":
        return json.loads(data.decode())
    else:
        return yaml.safe_load(data)


def _get_document(*, url: Optional[str] = None, path: Optional[Path] = None, timeout: int = 60) -> Dict[str, Any]:
    yaml_bytes: bytes
    content_type: Optional[str]
    if url is not None and path is not None:
        raise ValueError("Provide URL or Path, not both.")
    if url is not None:
        try:
            response = httpx.get(url, timeout=timeout)
            yaml_bytes = response.content
            if "content-type" in response.headers:
                content_type = response.headers["content-type"].split(";")[0]
            else:
                content_type = mimetypes.guess_type(url, strict=True)[0]

        except (httpx.HTTPError, httpcore.NetworkError) as e:
            raise ValueError("Could not get OpenAPI document from provided URL") from e
    elif path is not None:
        yaml_bytes = path.read_bytes()
        content_type = mimetypes.guess_type(path.absolute().as_uri(), strict=True)[0]

    else:
        raise ValueError("No URL or Path provided")

    return _load_yaml_or_json(yaml_bytes, content_type)
