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

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "some_file": some_file,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "BodyUploadFileTestsUploadPost":
        d = src_dict.copy()
        some_file = File(payload=BytesIO(d.pop("some_file")))

        body_upload_file_tests_upload_post = BodyUploadFileTestsUploadPost(
            some_file=some_file,
        )

        return body_upload_file_tests_upload_post
