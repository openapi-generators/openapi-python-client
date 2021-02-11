import urllib.parse
from typing import List, Union


class Pointer:
    """ https://tools.ietf.org/html/rfc6901 """

    def __init__(self, pointer: str) -> None:
        if pointer is None or pointer != "" and not pointer.startswith("/"):
            raise ValueError(f'Invalid pointer value {pointer}, it must match: *( "/" reference-token )')

        self._pointer = pointer

    @property
    def value(self) -> str:
        return self._pointer

    @property
    def parent(self) -> Union["Pointer", None]:
        tokens = self.tokens(False)

        if len(tokens) > 1:
            tokens.pop()
            return Pointer("/".join(tokens))
        else:
            assert tokens[-1] == ""
            return None

    def tokens(self, unescape: bool = True) -> List[str]:
        tokens = []

        if unescape:
            for token in self._pointer.split("/"):
                tokens.append(self._unescape(token))
        else:
            tokens = self._pointer.split("/")

        return tokens

    @property
    def unescapated_value(self) -> str:
        return self._unescape(self._pointer)

    def _unescape(self, data: str) -> str:
        data = urllib.parse.unquote(data)
        data = data.replace("~1", "/")
        data = data.replace("~0", "~")
        return data
