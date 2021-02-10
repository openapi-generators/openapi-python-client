import logging
import urllib
from pathlib import Path
from typing import Any, Dict, Generator, List, Union, cast

import httpx

from .data_loader import DataLoader
from .reference import Reference
from .resolved_schema import ResolvedSchema
from .resolver_types import SchemaData


class SchemaResolver:
    def __init__(self, url_or_path: Union[str, Path]):
        if not url_or_path:
            raise ValueError("Invalid document root reference, it shall be an remote url or local file path")

        self._root_path: Union[Path, None] = None
        self._root_path_dir: Union[Path, None] = None
        self._root_url: Union[str, None] = None
        self._root_url_scheme: Union[str, None] = None

        if self._isapath(url_or_path):
            url_or_path = cast(Path, url_or_path)
            self._root_path = url_or_path.absolute()
            self._root_path_dir = self._root_path.parent
        else:
            url_or_path = cast(str, url_or_path)
            self._root_url = url_or_path
            try:
                self._root_url_scheme = urllib.parse.urlparse(url_or_path).scheme
            except Exception:
                raise urllib.error.URLError(f"Coult not parse URL > {url_or_path}")

    def _isapath(self, url_or_path: Union[str, Path]) -> bool:
        return isinstance(url_or_path, Path)

    def resolve(self, recursive: bool = True) -> ResolvedSchema:
        assert self._root_path or self._root_url

        root_schema: SchemaData
        external_schemas: Dict[str, SchemaData] = {}
        errors: List[str] = []

        if self._root_path:
            root_schema = self._fetch_remote_file_path(self._root_path)
        elif self._root_url:
            root_schema = self._fetch_url_reference(self._root_url)

        self._resolve_schema_references(root_schema, external_schemas, errors, recursive)
        return ResolvedSchema(root_schema, external_schemas, errors)

    def _resolve_schema_references(
        self, root: SchemaData, external_schemas: Dict[str, SchemaData], errors: List[str], recursive: bool
    ) -> None:

        for ref in self._lookup_schema_references(root):
            if ref.is_local_ref():
                continue

            try:
                path = ref.value.split("#")[0]
                if path in external_schemas:
                    continue

                if ref.is_url_reference():
                    external_schemas[path] = self._fetch_url_reference(path)
                else:
                    external_schemas[path] = self._fetch_remote_reference(path)

                if recursive:
                    self._resolve_schema_references(external_schemas[path], external_schemas, errors, recursive)

            except Exception:
                errors.append("Failed to gather external reference data of {0}".format(ref.value))
                logging.exception("Failed to gather external reference data of {0}".format(ref.value))

    def _fetch_remote_reference(self, relative_path: str) -> SchemaData:
        assert self._root_path_dir or self._root_url

        if self._root_path_dir:
            abs_path = self._root_path_dir.joinpath(relative_path)
            return self._fetch_remote_file_path(abs_path)
        elif self._root_url:
            abs_url = urllib.parse.urljoin(self._root_url, relative_path)
            return self._fetch_url_reference(abs_url)
        else:
            raise RuntimeError("Bad object initilalization")

    def _fetch_remote_file_path(self, path: Path) -> SchemaData:
        logging.info(f"Fetching remote ref file path > {path}")
        return DataLoader.load(str(path), path.read_bytes())

    def _fetch_url_reference(self, url: str) -> SchemaData:
        if url.startswith("//", 0):
            url = "{0}:{1}".format(self._root_url_scheme, url)

        logging.info(f"Fetching remote ref url > {url}")
        return DataLoader.load(url, httpx.get(url).content)

    def _lookup_schema_references(self, attr: Any) -> Generator[Reference, None, None]:
        if isinstance(attr, dict):
            for key, val in attr.items():
                if key == "$ref":
                    yield Reference(val)
                else:
                    yield from self._lookup_schema_references(val)

        elif isinstance(attr, list):
            for val in attr:
                yield from self._lookup_schema_references(val)
