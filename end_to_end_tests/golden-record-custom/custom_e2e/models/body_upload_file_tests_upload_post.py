from io import BytesIO
from typing import Any, Dict

import attr

from ..types import File


@attr.s(auto_attribs=True)
class BodyUploadFileTestsUploadPost:
    """  """

    some_file: File

    def to_dict(self) -> Dict[str, Any]:
        some_file = self.some_file.to_tuple()

        field_dict = {
            "some_file": some_file,
        }

        return field_dict

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "BodyUploadFileTestsUploadPost":
        some_file = File(payload=BytesIO(d["some_file"]))

        return BodyUploadFileTestsUploadPost(
            some_file=some_file,
        )
