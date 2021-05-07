from io import BytesIO
from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, File, Unset

T = TypeVar("T", bound="BodyUploadFileTestsUploadPost")


@attr.s(auto_attribs=True)
class BodyUploadFileTestsUploadPost:
    """  """

    some_file: File
    some_string: Union[Unset, str] = "some_default_string"

    def to_dict(self) -> Dict[str, Any]:
        some_file = self.some_file.to_tuple()

        some_string = self.some_string

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "some_file": some_file,
            }
        )
        if some_string is not UNSET:
            field_dict["some_string"] = some_string

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        some_file = File(payload=BytesIO(d.pop("some_file")))

        some_string = d.pop("some_string", UNSET)

        body_upload_file_tests_upload_post = cls(
            some_file=some_file,
            some_string=some_string,
        )

        return body_upload_file_tests_upload_post
