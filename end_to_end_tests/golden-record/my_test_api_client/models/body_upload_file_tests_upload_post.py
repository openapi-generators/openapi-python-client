import datetime
import json
from io import BytesIO
from typing import TYPE_CHECKING, Any, Dict, List, Tuple, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.different_enum import DifferentEnum
from ..types import UNSET, File, FileJsonType, Unset

if TYPE_CHECKING:
    from ..models.a_form_data import AFormData
    from ..models.body_upload_file_tests_upload_post_additional_property import (
        BodyUploadFileTestsUploadPostAdditionalProperty,
    )
    from ..models.body_upload_file_tests_upload_post_some_nullable_object import (
        BodyUploadFileTestsUploadPostSomeNullableObject,
    )
    from ..models.body_upload_file_tests_upload_post_some_object import BodyUploadFileTestsUploadPostSomeObject
    from ..models.body_upload_file_tests_upload_post_some_optional_object import (
        BodyUploadFileTestsUploadPostSomeOptionalObject,
    )


T = TypeVar("T", bound="BodyUploadFileTestsUploadPost")


@_attrs_define
class BodyUploadFileTestsUploadPost:
    """
    Attributes:
        some_file (File):
        some_object (BodyUploadFileTestsUploadPostSomeObject):
        some_nullable_object (Union['BodyUploadFileTestsUploadPostSomeNullableObject', None]):
        some_optional_file (Union[Unset, File]):
        some_string (Union[Unset, str]):  Default: 'some_default_string'.
        a_datetime (Union[Unset, datetime.datetime]):
        a_date (Union[Unset, datetime.date]):
        some_number (Union[Unset, float]):
        some_array (Union[List['AFormData'], None, Unset]):
        some_optional_object (Union[Unset, BodyUploadFileTestsUploadPostSomeOptionalObject]):
        some_enum (Union[Unset, DifferentEnum]): An enumeration.
    """

    some_file: File
    some_object: "BodyUploadFileTestsUploadPostSomeObject"
    some_nullable_object: Union["BodyUploadFileTestsUploadPostSomeNullableObject", None]
    some_optional_file: Union[Unset, File] = UNSET
    some_string: Union[Unset, str] = "some_default_string"
    a_datetime: Union[Unset, datetime.datetime] = UNSET
    a_date: Union[Unset, datetime.date] = UNSET
    some_number: Union[Unset, float] = UNSET
    some_array: Union[List["AFormData"], None, Unset] = UNSET
    some_optional_object: Union[Unset, "BodyUploadFileTestsUploadPostSomeOptionalObject"] = UNSET
    some_enum: Union[Unset, DifferentEnum] = UNSET
    additional_properties: Dict[str, "BodyUploadFileTestsUploadPostAdditionalProperty"] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:
        from ..models.body_upload_file_tests_upload_post_some_nullable_object import (
            BodyUploadFileTestsUploadPostSomeNullableObject,
        )

        some_file = self.some_file.to_tuple()

        some_object = self.some_object.to_dict()

        some_nullable_object: Union[Dict[str, Any], None]
        if isinstance(self.some_nullable_object, BodyUploadFileTestsUploadPostSomeNullableObject):
            some_nullable_object = self.some_nullable_object.to_dict()
        else:
            some_nullable_object = self.some_nullable_object

        some_optional_file: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.some_optional_file, Unset):
            some_optional_file = self.some_optional_file.to_tuple()

        some_string = self.some_string

        a_datetime: Union[Unset, str] = UNSET
        if not isinstance(self.a_datetime, Unset):
            a_datetime = self.a_datetime.isoformat()

        a_date: Union[Unset, str] = UNSET
        if not isinstance(self.a_date, Unset):
            a_date = self.a_date.isoformat()

        some_number = self.some_number

        some_array: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.some_array, Unset):
            some_array = UNSET
        elif isinstance(self.some_array, list):
            some_array = []
            for some_array_type_0_item_data in self.some_array:
                some_array_type_0_item = some_array_type_0_item_data.to_dict()
                some_array.append(some_array_type_0_item)

        else:
            some_array = self.some_array

        some_optional_object: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.some_optional_object, Unset):
            some_optional_object = self.some_optional_object.to_dict()

        some_enum: Union[Unset, str] = UNSET
        if not isinstance(self.some_enum, Unset):
            some_enum = self.some_enum.value

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

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
        if a_datetime is not UNSET:
            field_dict["a_datetime"] = a_datetime
        if a_date is not UNSET:
            field_dict["a_date"] = a_date
        if some_number is not UNSET:
            field_dict["some_number"] = some_number
        if some_array is not UNSET:
            field_dict["some_array"] = some_array
        if some_optional_object is not UNSET:
            field_dict["some_optional_object"] = some_optional_object
        if some_enum is not UNSET:
            field_dict["some_enum"] = some_enum

        return field_dict

    def to_multipart(self) -> List[Tuple[str, Any]]:
        field_list: List[Tuple[str, Any]] = []
        some_file = self.some_file.to_tuple()

        field_list.append(("some_file", some_file))
        some_object = (None, json.dumps(self.some_object.to_dict()).encode(), "application/json")

        field_list.append(("some_object", some_object))
        some_nullable_object: Union[None, Tuple[None, bytes, str]]
        if isinstance(self.some_nullable_object, BodyUploadFileTestsUploadPostSomeNullableObject):
            some_nullable_object = (None, json.dumps(self.some_nullable_object.to_dict()).encode(), "application/json")
        else:
            some_nullable_object = self.some_nullable_object

        field_list.append(("some_nullable_object", some_nullable_object))
        some_optional_file: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.some_optional_file, Unset):
            some_optional_file = self.some_optional_file.to_tuple()

        if some_optional_file is not UNSET:
            field_list.append(("some_optional_file", some_optional_file))
        some_string = (
            self.some_string
            if isinstance(self.some_string, Unset)
            else (None, str(self.some_string).encode(), "text/plain")
        )

        if some_string is not UNSET:
            field_list.append(("some_string", some_string))
        a_datetime: Union[Unset, bytes] = UNSET
        if not isinstance(self.a_datetime, Unset):
            a_datetime = self.a_datetime.isoformat().encode()

        if a_datetime is not UNSET:
            field_list.append(("a_datetime", a_datetime))
        a_date: Union[Unset, bytes] = UNSET
        if not isinstance(self.a_date, Unset):
            a_date = self.a_date.isoformat().encode()

        if a_date is not UNSET:
            field_list.append(("a_date", a_date))
        some_number = (
            self.some_number
            if isinstance(self.some_number, Unset)
            else (None, str(self.some_number).encode(), "text/plain")
        )

        if some_number is not UNSET:
            field_list.append(("some_number", some_number))
        some_array: Union[None, Tuple[None, bytes, str], Unset]
        if isinstance(self.some_array, Unset):
            some_array = UNSET
        elif isinstance(self.some_array, list):
            _temp_some_array = []
            for some_array_type_0_item_data in self.some_array:
                some_array_type_0_item = some_array_type_0_item_data.to_dict()
                _temp_some_array.append(some_array_type_0_item)
            some_array = (None, json.dumps(_temp_some_array).encode(), "application/json")

        else:
            some_array = self.some_array

        if some_array is not UNSET:
            field_list.append(("some_array", some_array))
        some_optional_object: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.some_optional_object, Unset):
            some_optional_object = (None, json.dumps(self.some_optional_object.to_dict()).encode(), "application/json")

        if some_optional_object is not UNSET:
            field_list.append(("some_optional_object", some_optional_object))
        some_enum: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.some_enum, Unset):
            some_enum = (None, str(self.some_enum.value).encode(), "text/plain")

        if some_enum is not UNSET:
            field_list.append(("some_enum", some_enum))

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, json.dumps(prop.to_dict()).encode(), "application/json")

        field_list += list(field_dict.items())

        return field_list

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.a_form_data import AFormData
        from ..models.body_upload_file_tests_upload_post_additional_property import (
            BodyUploadFileTestsUploadPostAdditionalProperty,
        )
        from ..models.body_upload_file_tests_upload_post_some_nullable_object import (
            BodyUploadFileTestsUploadPostSomeNullableObject,
        )
        from ..models.body_upload_file_tests_upload_post_some_object import BodyUploadFileTestsUploadPostSomeObject
        from ..models.body_upload_file_tests_upload_post_some_optional_object import (
            BodyUploadFileTestsUploadPostSomeOptionalObject,
        )

        d = src_dict.copy()
        some_file = File(payload=BytesIO(d.pop("some_file")))

        some_object = BodyUploadFileTestsUploadPostSomeObject.from_dict(d.pop("some_object"))

        def _parse_some_nullable_object(data: object) -> Union["BodyUploadFileTestsUploadPostSomeNullableObject", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                some_nullable_object_type_0 = BodyUploadFileTestsUploadPostSomeNullableObject.from_dict(data)

                return some_nullable_object_type_0
            except:  # noqa: E722
                pass
            return cast(Union["BodyUploadFileTestsUploadPostSomeNullableObject", None], data)

        some_nullable_object = _parse_some_nullable_object(d.pop("some_nullable_object"))

        _some_optional_file = d.pop("some_optional_file", UNSET)
        some_optional_file: Union[Unset, File]
        if isinstance(_some_optional_file, Unset):
            some_optional_file = UNSET
        else:
            some_optional_file = File(payload=BytesIO(_some_optional_file))

        some_string = d.pop("some_string", UNSET)

        _a_datetime = d.pop("a_datetime", UNSET)
        a_datetime: Union[Unset, datetime.datetime]
        if isinstance(_a_datetime, Unset):
            a_datetime = UNSET
        else:
            a_datetime = isoparse(_a_datetime)

        _a_date = d.pop("a_date", UNSET)
        a_date: Union[Unset, datetime.date]
        if isinstance(_a_date, Unset):
            a_date = UNSET
        else:
            a_date = isoparse(_a_date).date()

        some_number = d.pop("some_number", UNSET)

        def _parse_some_array(data: object) -> Union[List["AFormData"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                some_array_type_0 = []
                _some_array_type_0 = data
                for some_array_type_0_item_data in _some_array_type_0:
                    some_array_type_0_item = AFormData.from_dict(some_array_type_0_item_data)

                    some_array_type_0.append(some_array_type_0_item)

                return some_array_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["AFormData"], None, Unset], data)

        some_array = _parse_some_array(d.pop("some_array", UNSET))

        _some_optional_object = d.pop("some_optional_object", UNSET)
        some_optional_object: Union[Unset, BodyUploadFileTestsUploadPostSomeOptionalObject]
        if isinstance(_some_optional_object, Unset):
            some_optional_object = UNSET
        else:
            some_optional_object = BodyUploadFileTestsUploadPostSomeOptionalObject.from_dict(_some_optional_object)

        _some_enum = d.pop("some_enum", UNSET)
        some_enum: Union[Unset, DifferentEnum]
        if isinstance(_some_enum, Unset):
            some_enum = UNSET
        else:
            some_enum = DifferentEnum(_some_enum)

        body_upload_file_tests_upload_post = cls(
            some_file=some_file,
            some_object=some_object,
            some_nullable_object=some_nullable_object,
            some_optional_file=some_optional_file,
            some_string=some_string,
            a_datetime=a_datetime,
            a_date=a_date,
            some_number=some_number,
            some_array=some_array,
            some_optional_object=some_optional_object,
            some_enum=some_enum,
        )

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = BodyUploadFileTestsUploadPostAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        body_upload_file_tests_upload_post.additional_properties = additional_properties
        return body_upload_file_tests_upload_post

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "BodyUploadFileTestsUploadPostAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "BodyUploadFileTestsUploadPostAdditionalProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
