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
        self._root_url: Union[str, None] = None
        self._root_url_scheme: Union[str, None] = None
        self._parent_path: str

        if self._isapath(url_or_path):
            url_or_path = cast(Path, url_or_path)
            self._root_path = url_or_path.absolute()
            self._parent_path = str(self._root_path.parent)
        else:
            url_or_path = cast(str, url_or_path)
            self._root_url = url_or_path
            self._parent_path = url_or_path
            try:
                self._root_url_scheme = urllib.parse.urlparse(url_or_path).scheme
                if self._root_url_scheme not in ["http", "https"]:
                    raise ValueError(f"Unsupported URL scheme '{self._root_url_scheme}', expecting http or https")
            except (TypeError, AttributeError):
                raise urllib.error.URLError(f"Coult not parse URL > {url_or_path}")

    def _isapath(self, url_or_path: Union[str, Path]) -> bool:
        return isinstance(url_or_path, Path)

    def resolve(self, recursive: bool = True) -> ResolvedSchema:
        assert self._root_path or self._root_url

        root_schema: SchemaData
        external_schemas: Dict[str, SchemaData] = {}
        errors: List[str] = []
        parent: str

        if self._root_path:
            root_schema = self._fetch_remote_file_path(self._root_path)
        elif self._root_url:
            root_schema = self._fetch_url_reference(self._root_url)

        self._resolve_schema_references(self._parent_path, root_schema, external_schemas, errors, recursive)
        return ResolvedSchema(root_schema, external_schemas, errors)

    def _resolve_schema_references(
        self,
        parent: str,
        root: SchemaData,
        external_schemas: Dict[str, SchemaData],
        errors: List[str],
        recursive: bool,
    ) -> None:

        for ref in self._lookup_schema_references(root):
            if ref.is_local():
                continue

            try:
                path = self._absolute_path(ref.path, parent)
                parent = self._parent(path)

                if path in external_schemas:
                    continue

                external_schemas[path] = self._fetch_remote_reference(path)

                if recursive:
                    self._resolve_schema_references(parent, external_schemas[path], external_schemas, errors, recursive)

            except Exception:
                errors.append(f"Failed to gather external reference data of {ref.value} from {path}")
                logging.exception(f"Failed to gather external reference data of {ref.value} from {path}")

    def _parent(self, abs_path: str) -> str:
        if abs_path.startswith("http", 0):
            return urllib.parse.urljoin(f"{abs_path}/", "..")
        else:
            path = Path(abs_path)
            return str(path.parent)

    def _absolute_path(self, relative_path: str, parent: str) -> str:
        if relative_path.startswith("http", 0):
            return relative_path

        if relative_path.startswith("//"):
            if parent.startswith("http"):
                scheme = urllib.parse.urlparse(parent).scheme
                return f"{scheme}:{relative_path}"
            else:
                scheme = self._root_url_scheme or "http"
                return f"{scheme}:{relative_path}"

        if parent.startswith("http"):
            return urllib.parse.urljoin(parent, relative_path)
        else:
            parent_dir = Path(parent)
            abs_path = parent_dir.joinpath(relative_path)
            abs_path = abs_path.resolve()
            return str(abs_path)

    def _fetch_remote_reference(self, abs_path: str) -> SchemaData:
        res: SchemaData

        if abs_path.startswith("http"):
            res = self._fetch_url_reference(abs_path)
        else:
            res = self._fetch_remote_file_path(Path(abs_path))

        return res

    def _fetch_remote_file_path(self, path: Path) -> SchemaData:
        logging.info(f"Fetching remote ref file path > {path}")
        return DataLoader.load(str(path), path.read_bytes())

    def _fetch_url_reference(self, url: str) -> SchemaData:
        if url.startswith("//", 0):
            url = "{0}:{1}".format((self._root_url_scheme or "http"), url)

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
