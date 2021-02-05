import httpcore
import httpx
import urllib
import logging

from typing import Any, Dict, Optional, Sequence, Union, Generator, NewType
from pathlib import Path

from .resolver_types import SchemaData
from .reference import Reference
from .resolved_schema import ResolvedSchema
from .data_loader import DataLoader

class SchemaResolver:

    def __init__(self, url_or_path: Union[str, Path]):
        if not url_or_path:
            raise ValueError('Invalid document root reference, it shall be an remote url or local file path')
        
        self._root_path: Optional[Path] = None
        self._root_path_dir: Optional[Path] = None
        self._root_url: Optional[str] = None
        self._root_url_scheme: Optional[str] = None

        if isinstance(url_or_path, Path):
            self._root_path = url_or_path.absolute()
            self._root_path_dir = self._root_path.parent
        else:
            self._root_url = url_or_path
            self._root_url_scheme = urllib.parse.urlparse(url_or_path).scheme
        
    def resolve(self, recursive: bool = True) -> ResolvedSchema:
        root_schema: SchemaData
        external_schemas: Dict[str, SchemaData] = {}
        errors: Sequence[str] = []

        if self._root_path:
            root_schema = self._fetch_remote_file_path(self._root_path)
        else:
            root_schema = self._fetch_url_reference(self._root_url)

        self._resolve_schema_references(root_schema, external_schemas, errors, recursive)
        return ResolvedSchema(root_schema, external_schemas, errors)

    def _resolve_schema_references(self, root: SchemaData, external_schemas: Dict[str, SchemaData], errors: Sequence[str], recursive: bool) -> Sequence[SchemaData]:

        for ref in self._lookup_schema_references(root):
            if ref.is_local_ref():
                continue

            try:
                path = ref.value.split('#')[0]
                if path in external_schemas:
                    continue

                if ref.is_url_reference():
                    external_schemas[path] = self._fetch_url_reference(path)
                else:
                    external_schemas[path] = self._fetch_remote_reference(path)

                if recursive:
                    self._resolve_schema_references(external_schemas[path], external_schemas, errors, recursive)

            except Exception as e:
                errors.append('Failed to gather external reference data of {0}'.format(ref.value))
                logging.exception('Failed to gather external reference data of {0}'.format(ref.value))
    
    def _fetch_remote_reference(self, relative_path: str) -> SchemaData:
        if self._root_path:
            abs_path = self._root_path_dir.joinpath(relative_path)
            return self._fetch_remote_file_path(abs_path)
        else:
            abs_url = urllib.parse.urljoin(self._root_url, relative_path)
            return self._fetch_url_reference(abs_url)

    def _fetch_remote_file_path(self, path: Path) -> SchemaData:
        logging.info('Fetching remote ref file path > {0}'.format(path))
        return DataLoader.load(str(path), path.read_bytes())

    def _fetch_url_reference(self, url: str) -> SchemaData:
        if url.startswith('//', 0):
            url = "{0}{1}".format(self._root_url_scheme, url)

        logging.info('Fetching remote ref url > {0}'.format(url))
        return DataLoader.load(url, httpx.get(url).content)

    def _lookup_schema_references(self, attr: Any) -> Generator[Reference, None, None]:
        if isinstance(attr, dict):
            for key, val in attr.items():
                if key == '$ref':
                    yield Reference(val)
                else:
                    yield from self._lookup_schema_references(val)

        elif isinstance(attr, list):
            for val in attr:
                yield from self._lookup_schema_references(val)

