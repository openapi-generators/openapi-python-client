import urllib
from typing import Union


class Reference:
    def __init__(self, reference: str):
        self._ref = reference

    @property
    def remote_relative_path(self) -> Union[str, None]:
        if self.is_remote_ref():
            return self._ref.split("#")[0]
        return None

    @property
    def path_parent(self) -> str:
        path = self.path
        parts = path.split("/")
        parts.pop()
        return "/".join(parts)

    @property
    def path(self) -> str:
        d = self._ref.split("#")[-1]
        d = urllib.parse.unquote(d)
        d = d.replace("~1", "/")
        return d

    @property
    def value(self) -> str:
        return self._ref

    def is_relative_reference(self) -> bool:
        return self.is_remote_ref() and not self.is_url_reference()

    def is_url_reference(self) -> bool:
        return self.is_remote_ref() and (self._ref.startswith("//", 0) or self._ref.startswith("http", 0))

    def is_remote_ref(self) -> bool:
        return not self.is_local_ref()

    def is_local_ref(self) -> bool:
        return self._ref.startswith("#", 0)
