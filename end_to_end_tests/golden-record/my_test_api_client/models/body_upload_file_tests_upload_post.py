import json
from io import BytesIO
from typing import Any, Dict, List, Optional, Type, TypeVar, Union, cast

import attr

from ..models.body_upload_file_tests_upload_post_some_nullable_object import (
    BodyUploadFileTestsUploadPostSomeNullableObject,
)
from ..models.body_upload_file_tests_upload_post_some_object import BodyUploadFileTestsUploadPostSomeObject
from ..models.body_upload_file_tests_upload_post_some_optional_object import (
    BodyUploadFileTestsUploadPostSomeOptionalObject,
)
from ..types import UNSET, File, FileJsonType, Unset

T = TypeVar("T", bound="BodyUploadFileTestsUploadPost")


@attr.s(auto_attribs=True)
class BodyUploadFileTestsUploadPost:
    """ """

    some_file: File
    some_object: BodyUploadFileTestsUploadPostSomeObject
    some_nullable_object: Optional[BodyUploadFileTestsUploadPostSomeNullableObject]
    some_optional_file: Union[Unset, File] = UNSET
    some_string: Union[Unset, str] = "some_default_string"
    some_number: Union[Unset, float] = UNSET
    some_array: Union[Unset, List[float]] = UNSET
    some_optional_object: Union[Unset, BodyUploadFileTestsUploadPostSomeOptionalObject] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        some_file = self.some_file.to_tuple()

        some_object = self.some_object.to_dict()

        some_optional_file: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.some_optional_file, Unset):
            some_optional_file = self.some_optional_file.to_tuple()

        some_string = self.some_string
        some_number = self.some_number
        some_array: Union[Unset, List[float]] = UNSET
        if not isinstance(self.some_array, Unset):
            some_array = self.some_array

        some_optional_object: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.some_optional_object, Unset):
            some_optional_object = self.some_optional_object.to_dict()

        some_nullable_object = self.some_nullable_object.to_dict() if self.some_nullable_object else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "some_file": some_file,
                "some_object": some_object,
                "some_nullable_object": some_nullable_object,
            }
        )
        if some_optional_file is not UNSET:
            field_dict["some_optional_file"] = some_optional_file
        if some_string is not UNSET:
            field_dict["some_string"] = some_string
        if some_number is not UNSET:
            field_dict["some_number"] = some_number
        if some_array is not UNSET:
            field_dict["some_array"] = some_array
        if some_optional_object is not UNSET:
            field_dict["some_optional_object"] = some_optional_object

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        some_file = self.some_file.to_tuple()

        some_object = (None, json.dumps(self.some_object.to_dict()), "application/json")

        some_optional_file = UNSET
        if not isinstance(self.some_optional_file, Unset):
            some_optional_file = self.some_optional_file.to_tuple()

        some_string = self.some_string
        some_number = self.some_number
        some_array = UNSET
        if not isinstance(self.some_array, Unset):
            some_array = self.some_array
            some_array = (None, json.dumps(some_array), "application/json")

        some_optional_object = UNSET
        if not isinstance(self.some_optional_object, Unset):
            some_optional_object = (None, json.dumps(self.some_optional_object.to_dict()), "application/json")

        some_nullable_object = (
            (None, json.dumps(self.some_nullable_object.to_dict()), "application/json")
            if self.some_nullable_object
            else None
        )

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "some_file": some_file,
                "some_object": some_object,
                "some_nullable_object": some_nullable_object,
            }
        )
        if some_optional_file is not UNSET:
            field_dict["some_optional_file"] = some_optional_file
        if some_string is not UNSET:
            field_dict["some_string"] = some_string
        if some_number is not UNSET:
            field_dict["some_number"] = some_number
        if some_array is not UNSET:
            field_dict["some_array"] = some_array
        if some_optional_object is not UNSET:
            field_dict["some_optional_object"] = some_optional_object

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        some_file = File(payload=BytesIO(d.pop("some_file")))

        some_object = BodyUploadFileTestsUploadPostSomeObject.from_dict(d.pop("some_object"))

        _some_optional_file = d.pop("some_optional_file", UNSET)
        some_optional_file: Union[Unset, File]
        if isinstance(_some_optional_file, Unset):
            some_optional_file = UNSET
        else:
            some_optional_file = File(payload=BytesIO(_some_optional_file))

        some_string = d.pop("some_string", UNSET)

        some_number = d.pop("some_number", UNSET)

        some_array = cast(List[float], d.pop("some_array", UNSET))

        _some_optional_object = d.pop("some_optional_object", UNSET)
        some_optional_object: Union[Unset, BodyUploadFileTestsUploadPostSomeOptionalObject]
        if isinstance(_some_optional_object, Unset):
            some_optional_object = UNSET
        else:
            some_optional_object = BodyUploadFileTestsUploadPostSomeOptionalObject.from_dict(_some_optional_object)

        _some_nullable_object = d.pop("some_nullable_object")
        some_nullable_object: Optional[BodyUploadFileTestsUploadPostSomeNullableObject]
        if _some_nullable_object is None:
            some_nullable_object = None
        else:
            some_nullable_object = BodyUploadFileTestsUploadPostSomeNullableObject.from_dict(_some_nullable_object)

        body_upload_file_tests_upload_post = cls(
            some_file=some_file,
            some_object=some_object,
            some_optional_file=some_optional_file,
            some_string=some_string,
            some_number=some_number,
            some_array=some_array,
            some_optional_object=some_optional_object,
            some_nullable_object=some_nullable_object,
        )

        return body_upload_file_tests_upload_post
