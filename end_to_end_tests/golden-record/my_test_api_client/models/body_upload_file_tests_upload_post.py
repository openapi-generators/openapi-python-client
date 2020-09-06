from typing import Any, Dict

import attr

from ..types import File


@attr.s(auto_attribs=True)
class BodyUploadFileTestsUploadPost:
    """  """

    some_file: File

    def to_dict(self) -> Dict[str, Any]:
        some_file = self.some_file.to_tuple()

        return {
            "some_file": some_file,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "BodyUploadFileTestsUploadPost":
        some_file = d["some_file"]

        return BodyUploadFileTestsUploadPost(
            some_file=some_file,
        )
