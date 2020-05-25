from __future__ import annotations

from dataclasses import astuple, dataclass
from typing import Any, Dict

from .types import File


@dataclass
class BodyUploadFileTestsUploadPost:
    """  """

    some_file: File

    def to_dict(self) -> Dict[str, Any]:
        some_file = self.some_file.to_tuple()

        return {
            "some_file": some_file,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> BodyUploadFileTestsUploadPost:
        some_file = d["some_file"]

        return BodyUploadFileTestsUploadPost(some_file=some_file,)
