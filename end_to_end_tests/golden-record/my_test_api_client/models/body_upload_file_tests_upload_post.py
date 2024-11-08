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
        some_required_number (float):
        some_object (BodyUploadFileTestsUploadPostSomeObject):
        some_nullable_object (Union['BodyUploadFileTestsUploadPostSomeNullableObject', None]):
        some_optional_file (Union[Unset, File]):
        some_string (Union[Unset, str]):  Default: 'some_default_string'.
        a_datetime (Union[Unset, datetime.datetime]):
        a_date (Union[Unset, datetime.date]):
        some_number (Union[Unset, float]):
        some_nullable_number (Union[None, Unset, float]):
        some_int_array (Union[Unset, List[Union[None, int]]]):
        some_array (Union[List['AFormData'], None, Unset]):
        some_optional_object (Union[Unset, BodyUploadFileTestsUploadPostSomeOptionalObject]):
        some_enum (Union[Unset, DifferentEnum]): An enumeration.
    """

    some_file: File
    some_required_number: float
    some_object: "BodyUploadFileTestsUploadPostSomeObject"
    some_nullable_object: Union["BodyUploadFileTestsUploadPostSomeNullableObject", None]
    some_optional_file: Union[Unset, File] = UNSET
    some_string: Union[Unset, str] = "some_default_string"
    a_datetime: Union[Unset, datetime.datetime] = UNSET
    a_date: Union[Unset, datetime.date] = UNSET
    some_number: Union[Unset, float] = UNSET
    some_nullable_number: Union[None, Unset, float] = UNSET
    some_int_array: Union[Unset, List[Union[None, int]]] = UNSET
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

        prop1 = self.some_file.to_tuple()

        prop2 = self.some_required_number
        prop3 = self.some_object.to_dict()
        prop4: Union[Dict[str, Any], None]
        if isinstance(self.some_nullable_object, BodyUploadFileTestsUploadPostSomeNullableObject):
            prop4 = self.some_nullable_object.to_dict()
        else:
            prop4 = self.some_nullable_object
        prop5: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.some_optional_file, Unset):
            prop5 = self.some_optional_file.to_tuple()

        prop6 = self.some_string
        prop7: Union[Unset, str] = UNSET
        if not isinstance(self.a_datetime, Unset):
            prop7 = self.a_datetime.isoformat()
        prop8: Union[Unset, str] = UNSET
        if not isinstance(self.a_date, Unset):
            prop8 = self.a_date.isoformat()
        prop9 = self.some_number
        prop10: Union[None, Unset, float]
        if isinstance(self.some_nullable_number, Unset):
            prop10 = UNSET
        else:
            prop10 = self.some_nullable_number
        prop11: Union[Unset, List[Union[None, int]]] = UNSET
        if not isinstance(self.some_int_array, Unset):
            prop11 = []
            for some_int_array_item_data in self.some_int_array:
                some_int_array_item: Union[None, int]
                some_int_array_item = some_int_array_item_data
                prop11.append(some_int_array_item)

        prop12: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.some_array, Unset):
            prop12 = UNSET
        elif isinstance(self.some_array, list):
            prop12 = []
            for some_array_type_0_item_data in self.some_array:
                some_array_type_0_item = some_array_type_0_item_data.to_dict()
                prop12.append(some_array_type_0_item)

        else:
            prop12 = self.some_array
        prop13: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.some_optional_object, Unset):
            prop13 = self.some_optional_object.to_dict()
        prop14: Union[Unset, str] = UNSET
        if not isinstance(self.some_enum, Unset):
            prop14 = self.some_enum.value

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()
        field_dict = {
            **field_dict,
            "some_file": prop1,
            "some_required_number": prop2,
            "some_object": prop3,
            "some_nullable_object": prop4,
            **({} if prop5 is UNSET else {"some_optional_file": prop5}),
            **({} if prop6 is UNSET else {"some_string": prop6}),
            **({} if prop7 is UNSET else {"a_datetime": prop7}),
            **({} if prop8 is UNSET else {"a_date": prop8}),
            **({} if prop9 is UNSET else {"some_number": prop9}),
            **({} if prop10 is UNSET else {"some_nullable_number": prop10}),
            **({} if prop11 is UNSET else {"some_int_array": prop11}),
            **({} if prop12 is UNSET else {"some_array": prop12}),
            **({} if prop13 is UNSET else {"some_optional_object": prop13}),
            **({} if prop14 is UNSET else {"some_enum": prop14}),
        }

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        prop1 = self.some_file.to_tuple()

        prop2 = (None, str(self.some_required_number).encode(), "text/plain")

        prop3 = (None, json.dumps(self.some_object.to_dict()).encode(), "application/json")
        prop4: Tuple[None, bytes, str]

        if isinstance(self.some_nullable_object, BodyUploadFileTestsUploadPostSomeNullableObject):
            prop4 = (None, json.dumps(self.some_nullable_object.to_dict()).encode(), "application/json")
        else:
            prop4 = (None, str(self.some_nullable_object).encode(), "text/plain")

        prop5: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.some_optional_file, Unset):
            prop5 = self.some_optional_file.to_tuple()

        prop6 = (
            self.some_string
            if isinstance(self.some_string, Unset)
            else (None, str(self.some_string).encode(), "text/plain")
        )

        prop7: Union[Unset, bytes] = UNSET
        if not isinstance(self.a_datetime, Unset):
            prop7 = self.a_datetime.isoformat().encode()
        prop8: Union[Unset, bytes] = UNSET
        if not isinstance(self.a_date, Unset):
            prop8 = self.a_date.isoformat().encode()
        prop9 = (
            self.some_number
            if isinstance(self.some_number, Unset)
            else (None, str(self.some_number).encode(), "text/plain")
        )

        prop10: Union[Tuple[None, bytes, str], Unset]

        if isinstance(self.some_nullable_number, Unset):
            prop10 = UNSET
        elif isinstance(self.some_nullable_number, float):
            prop10 = (None, str(self.some_nullable_number).encode(), "text/plain")
        else:
            prop10 = (None, str(self.some_nullable_number).encode(), "text/plain")

        prop11: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.some_int_array, Unset):
            _temp_prop11 = []
            for some_int_array_item_data in self.some_int_array:
                some_int_array_item: Union[None, int]
                some_int_array_item = some_int_array_item_data
                _temp_prop11.append(some_int_array_item)
            prop11 = (None, json.dumps(_temp_prop11).encode(), "application/json")

        prop12: Union[Tuple[None, bytes, str], Unset]

        if isinstance(self.some_array, Unset):
            prop12 = UNSET
        elif isinstance(self.some_array, list):
            _temp_prop12 = []
            for some_array_type_0_item_data in self.some_array:
                some_array_type_0_item = some_array_type_0_item_data.to_dict()
                _temp_prop12.append(some_array_type_0_item)
            prop12 = (None, json.dumps(_temp_prop12).encode(), "application/json")
        else:
            prop12 = (None, str(self.some_array).encode(), "text/plain")

        prop13: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.some_optional_object, Unset):
            prop13 = (None, json.dumps(self.some_optional_object.to_dict()).encode(), "application/json")
        prop14: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.some_enum, Unset):
            prop14 = (None, str(self.some_enum.value).encode(), "text/plain")

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, json.dumps(prop.to_dict()).encode(), "application/json")
        field_dict = {
            **field_dict,
            "some_file": prop1,
            "some_required_number": prop2,
            "some_object": prop3,
            "some_nullable_object": prop4,
            **({} if prop5 is UNSET else {"some_optional_file": prop5}),
            **({} if prop6 is UNSET else {"some_string": prop6}),
            **({} if prop7 is UNSET else {"a_datetime": prop7}),
            **({} if prop8 is UNSET else {"a_date": prop8}),
            **({} if prop9 is UNSET else {"some_number": prop9}),
            **({} if prop10 is UNSET else {"some_nullable_number": prop10}),
            **({} if prop11 is UNSET else {"some_int_array": prop11}),
            **({} if prop12 is UNSET else {"some_array": prop12}),
            **({} if prop13 is UNSET else {"some_optional_object": prop13}),
            **({} if prop14 is UNSET else {"some_enum": prop14}),
        }

        return field_dict

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

        some_required_number = d.pop("some_required_number")

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

        def _parse_some_nullable_number(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        some_nullable_number = _parse_some_nullable_number(d.pop("some_nullable_number", UNSET))

        some_int_array = []
        _some_int_array = d.pop("some_int_array", UNSET)
        for some_int_array_item_data in _some_int_array or []:

            def _parse_some_int_array_item(data: object) -> Union[None, int]:
                if data is None:
                    return data
                return cast(Union[None, int], data)

            some_int_array_item = _parse_some_int_array_item(some_int_array_item_data)

            some_int_array.append(some_int_array_item)

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
            some_required_number=some_required_number,
            some_object=some_object,
            some_nullable_object=some_nullable_object,
            some_optional_file=some_optional_file,
            some_string=some_string,
            a_datetime=a_datetime,
            a_date=a_date,
            some_number=some_number,
            some_nullable_number=some_nullable_number,
            some_int_array=some_int_array,
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
