from typing import Any, Dict, Optional, Sequence, Union
from .resolver_types import SchemaData


class ResolvedSchema:

    def __init__(self, root, refs, errors):
        self._root: SchemaData = root
        self._refs: Dict[str, SchemaData] = refs
        self._errors: Sequense[str] = errors

        self._resolved_schema: SchemaData = self._root
        self._process()

    @property
    def schema(self) -> SchemaData:
        return self._resolved_schema

    @property
    def errors(self) -> Sequence[str]:
        return self._errors.copy()

    def _process(self):
        pass

