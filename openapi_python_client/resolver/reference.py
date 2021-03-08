import urllib.parse
from pathlib import Path
from typing import Union

from .pointer import Pointer


class Reference:
    """ https://tools.ietf.org/html/draft-pbryan-zyp-json-ref-03 """

    def __init__(self, reference: str, parent: str = None):
        self._ref = reference
        self._parsed_ref = urllib.parse.urlparse(reference)
        self._parent = parent

    @property
    def path(self) -> str:
        return urllib.parse.urldefrag(self._parsed_ref.geturl()).url

    @property
    def abs_path(self) -> str:
        if self._parent:
            parent_dir = Path(self._parent)
            abs_path = parent_dir.joinpath(self.path)
            abs_path = abs_path.resolve()
            return str(abs_path)
        else:
            return self.path

    @property
    def parent(self) -> Union[str, None]:
        return self._parent

    @property
    def pointer(self) -> Pointer:
        frag = self._parsed_ref.fragment
        if self.is_url() and frag != "" and not frag.startswith("/"):
            frag = f"/{frag}"

        return Pointer(frag)

    def is_relative(self) -> bool:
        """ return True if reference path is a relative path """
        return not self.is_absolute()

    def is_absolute(self) -> bool:
        """ return True is reference path is an absolute path """
        return self._parsed_ref.netloc != ""

    @property
    def value(self) -> str:
        return self._ref

    def is_url(self) -> bool:
        """ return True if the reference path is pointing to an external url location """
        return self.is_remote() and self._parsed_ref.netloc != ""

    def is_remote(self) -> bool:
        """ return True if the reference pointer is pointing to a remote document """
        return not self.is_local()

    def is_local(self) -> bool:
        """ return True if the reference pointer is pointing to the current document """
        return self._parsed_ref.path == ""

    def is_full_document(self) -> bool:
        """ return True if the reference pointer is pointing to the whole document content """
        return self.pointer.parent is None
