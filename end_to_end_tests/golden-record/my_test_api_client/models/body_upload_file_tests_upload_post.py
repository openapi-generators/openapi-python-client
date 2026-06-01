from __future__ import annotations

import datetime
import json
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from pydantic import ConfigDict
from tandem_platform.schema.protected import BaseModel

from .. import types
from ..models.different_enum import DifferentEnum
from ..types import File

if TYPE_CHECKING:
    from ..models.a_form_data import AFormData
    from ..models.body_upload_file_tests_upload_post_some_nullable_object import (
        BodyUploadFileTestsUploadPostSomeNullableObject,
    )
    from ..models.body_upload_file_tests_upload_post_some_object import BodyUploadFileTestsUploadPostSomeObject
    from ..models.body_upload_file_tests_upload_post_some_optional_object import (
        BodyUploadFileTestsUploadPostSomeOptionalObject,
    )


T = TypeVar("T", bound="BodyUploadFileTestsUploadPost")


class BodyUploadFileTestsUploadPost(BaseModel):
    """
    Attributes:
        some_file (File):
        some_required_number (float):
        some_object (BodyUploadFileTestsUploadPostSomeObject):
        some_nullable_object (BodyUploadFileTestsUploadPostSomeNullableObject | None):
        some_optional_file (File | Unset):
        some_string (str | Unset):  Default: 'some_default_string'.
        a_datetime (datetime.datetime | Unset):
        a_date (datetime.date | Unset):
        some_number (float | Unset):
        some_nullable_number (float | None | Unset):
        some_int_array (list[int | None] | Unset):
        some_array (list[AFormData] | None | Unset):
        some_optional_object (BodyUploadFileTestsUploadPostSomeOptionalObject | Unset):
        some_enum (DifferentEnum | Unset): An enumeration.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    some_file: File
    some_required_number: float
    some_object: BodyUploadFileTestsUploadPostSomeObject
    some_nullable_object: BodyUploadFileTestsUploadPostSomeNullableObject | None
    some_optional_file: File | None = None
    some_string: str | None = "some_default_string"
    a_datetime: datetime.datetime | None = None
    a_date: datetime.date | None = None
    some_number: float | None = None
    some_nullable_number: float | None = None
    some_int_array: list[int | None] | None = None
    some_array: list[AFormData] | None = None
    some_optional_object: BodyUploadFileTestsUploadPostSomeOptionalObject | None = None
    some_enum: DifferentEnum | None = None

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_unset=True, mode="json")

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        files.append(("some_file", self.some_file.to_tuple()))

        files.append(("some_required_number", (None, str(self.some_required_number).encode(), "text/plain")))

        files.append(("some_object", (None, json.dumps(self.some_object.to_dict()).encode(), "application/json")))

        if isinstance(self.some_nullable_object, BodyUploadFileTestsUploadPostSomeNullableObject):
            files.append(
                (
                    "some_nullable_object",
                    (None, json.dumps(self.some_nullable_object.to_dict()).encode(), "application/json"),
                )
            )
        else:
            files.append(("some_nullable_object", (None, str(self.some_nullable_object).encode(), "text/plain")))

        if "some_optional_file" in self.model_fields_set and self.some_optional_file is not None:
            files.append(("some_optional_file", self.some_optional_file.to_tuple()))

        if "some_string" in self.model_fields_set and self.some_string is not None:
            files.append(("some_string", (None, str(self.some_string).encode(), "text/plain")))

        if "a_datetime" in self.model_fields_set and self.a_datetime is not None:
            files.append(("a_datetime", (None, self.a_datetime.isoformat().encode(), "text/plain")))

        if "a_date" in self.model_fields_set and self.a_date is not None:
            files.append(("a_date", (None, self.a_date.isoformat().encode(), "text/plain")))

        if "some_number" in self.model_fields_set and self.some_number is not None:
            files.append(("some_number", (None, str(self.some_number).encode(), "text/plain")))

        if "some_nullable_number" in self.model_fields_set and self.some_nullable_number is not None:
            if isinstance(self.some_nullable_number, float):
                files.append(("some_nullable_number", (None, str(self.some_nullable_number).encode(), "text/plain")))
            else:
                files.append(("some_nullable_number", (None, str(self.some_nullable_number).encode(), "text/plain")))

        if "some_int_array" in self.model_fields_set and self.some_int_array is not None:
            for some_int_array_item_element in self.some_int_array:
                if isinstance(some_int_array_item_element, int):
                    files.append(("some_int_array", (None, str(some_int_array_item_element).encode(), "text/plain")))
                else:
                    files.append(("some_int_array", (None, str(some_int_array_item_element).encode(), "text/plain")))

        if "some_array" in self.model_fields_set and self.some_array is not None:
            if isinstance(self.some_array, list):
                for some_array_type_0_item_element in self.some_array:
                    files.append(
                        (
                            "some_array",
                            (None, json.dumps(some_array_type_0_item_element.to_dict()).encode(), "application/json"),
                        )
                    )
            else:
                files.append(("some_array", (None, str(self.some_array).encode(), "text/plain")))

        if "some_optional_object" in self.model_fields_set and self.some_optional_object is not None:
            files.append(
                (
                    "some_optional_object",
                    (None, json.dumps(self.some_optional_object.to_dict()).encode(), "application/json"),
                )
            )

        if "some_enum" in self.model_fields_set and self.some_enum is not None:
            files.append(("some_enum", (None, str(self.some_enum.value).encode(), "text/plain")))

        for prop_name, prop in (self.__pydantic_extra__ or {}).items():
            files.append((prop_name, (None, json.dumps(prop.to_dict()).encode(), "application/json")))

        return files


from ..models.a_form_data import AFormData
from ..models.body_upload_file_tests_upload_post_some_nullable_object import (
    BodyUploadFileTestsUploadPostSomeNullableObject,
)
from ..models.body_upload_file_tests_upload_post_some_object import BodyUploadFileTestsUploadPostSomeObject
from ..models.body_upload_file_tests_upload_post_some_optional_object import (
    BodyUploadFileTestsUploadPostSomeOptionalObject,
)

BodyUploadFileTestsUploadPost.model_rebuild()
