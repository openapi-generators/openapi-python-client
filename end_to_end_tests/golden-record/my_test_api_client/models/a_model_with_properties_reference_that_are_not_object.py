import datetime
from io import BytesIO
from typing import Any, BinaryIO, Dict, List, Optional, TextIO, Tuple, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.an_enum import AnEnum
from ..types import UNSET, File, Unset

T = TypeVar("T", bound="AModelWithPropertiesReferenceThatAreNotObject")


@attr.s(auto_attribs=True)
class AModelWithPropertiesReferenceThatAreNotObject:
    """ """

    enum_properties_ref: Union[Unset, List[AnEnum]] = UNSET
    str_properties_ref: Union[Unset, List[str]] = UNSET
    date_properties_ref: Union[Unset, List[datetime.date]] = UNSET
    datetime_properties_ref: Union[Unset, List[datetime.datetime]] = UNSET
    int_32_properties_ref: Union[Unset, List[int]] = UNSET
    int_64_properties_ref: Union[Unset, List[int]] = UNSET
    float_properties_ref: Union[Unset, List[float]] = UNSET
    double_properties_ref: Union[Unset, List[float]] = UNSET
    file_properties_ref: Union[Unset, List[File]] = UNSET
    bytestream_properties_ref: Union[Unset, List[str]] = UNSET
    enum_properties: Union[Unset, List[AnEnum]] = UNSET
    str_properties: Union[Unset, List[str]] = UNSET
    date_properties: Union[Unset, List[datetime.date]] = UNSET
    datetime_properties: Union[Unset, List[datetime.datetime]] = UNSET
    int_32_properties: Union[Unset, List[int]] = UNSET
    int_64_properties: Union[Unset, List[int]] = UNSET
    float_properties: Union[Unset, List[float]] = UNSET
    double_properties: Union[Unset, List[float]] = UNSET
    file_properties: Union[Unset, List[File]] = UNSET
    bytestream_properties: Union[Unset, List[str]] = UNSET
    enum_property_ref: Union[Unset, AnEnum] = UNSET
    str_property_ref: Union[Unset, str] = UNSET
    date_property_ref: Union[Unset, datetime.date] = UNSET
    datetime_property_ref: Union[Unset, datetime.datetime] = UNSET
    int_32_property_ref: Union[Unset, int] = UNSET
    int_64_property_ref: Union[Unset, int] = UNSET
    float_property_ref: Union[Unset, float] = UNSET
    double_property_ref: Union[Unset, float] = UNSET
    file_property_ref: Union[Unset, File] = UNSET
    bytestream_property_ref: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        enum_properties_ref: Union[Unset, List[str]] = UNSET
        if not isinstance(self.enum_properties_ref, Unset):
            enum_properties_ref = []
            for componentsschemas_an_other_array_of_enum_item_data in self.enum_properties_ref:
                componentsschemas_an_other_array_of_enum_item = componentsschemas_an_other_array_of_enum_item_data.value

                enum_properties_ref.append(componentsschemas_an_other_array_of_enum_item)

        str_properties_ref: Union[Unset, List[str]] = UNSET
        if not isinstance(self.str_properties_ref, Unset):
            str_properties_ref = self.str_properties_ref

        date_properties_ref: Union[Unset, List[str]] = UNSET
        if not isinstance(self.date_properties_ref, Unset):
            date_properties_ref = []
            for componentsschemas_an_other_array_of_date_item_data in self.date_properties_ref:
                componentsschemas_an_other_array_of_date_item = (
                    componentsschemas_an_other_array_of_date_item_data.isoformat()
                )
                date_properties_ref.append(componentsschemas_an_other_array_of_date_item)

        datetime_properties_ref: Union[Unset, List[str]] = UNSET
        if not isinstance(self.datetime_properties_ref, Unset):
            datetime_properties_ref = []
            for componentsschemas_an_other_array_of_date_time_item_data in self.datetime_properties_ref:
                componentsschemas_an_other_array_of_date_time_item = (
                    componentsschemas_an_other_array_of_date_time_item_data.isoformat()
                )

                datetime_properties_ref.append(componentsschemas_an_other_array_of_date_time_item)

        int_32_properties_ref: Union[Unset, List[int]] = UNSET
        if not isinstance(self.int_32_properties_ref, Unset):
            int_32_properties_ref = self.int_32_properties_ref

        int_64_properties_ref: Union[Unset, List[int]] = UNSET
        if not isinstance(self.int_64_properties_ref, Unset):
            int_64_properties_ref = self.int_64_properties_ref

        float_properties_ref: Union[Unset, List[float]] = UNSET
        if not isinstance(self.float_properties_ref, Unset):
            float_properties_ref = self.float_properties_ref

        double_properties_ref: Union[Unset, List[float]] = UNSET
        if not isinstance(self.double_properties_ref, Unset):
            double_properties_ref = self.double_properties_ref

        file_properties_ref: Union[Unset, List[Tuple[Optional[str], Union[BinaryIO, TextIO], Optional[str]]]] = UNSET
        if not isinstance(self.file_properties_ref, Unset):
            file_properties_ref = []
            for componentsschemas_an_other_array_of_file_item_data in self.file_properties_ref:
                componentsschemas_an_other_array_of_file_item = (
                    componentsschemas_an_other_array_of_file_item_data.to_tuple()
                )

                file_properties_ref.append(componentsschemas_an_other_array_of_file_item)

        bytestream_properties_ref: Union[Unset, List[str]] = UNSET
        if not isinstance(self.bytestream_properties_ref, Unset):
            bytestream_properties_ref = self.bytestream_properties_ref

        enum_properties: Union[Unset, List[str]] = UNSET
        if not isinstance(self.enum_properties, Unset):
            enum_properties = []
            for componentsschemas_an_array_of_enum_item_data in self.enum_properties:
                componentsschemas_an_array_of_enum_item = componentsschemas_an_array_of_enum_item_data.value

                enum_properties.append(componentsschemas_an_array_of_enum_item)

        str_properties: Union[Unset, List[str]] = UNSET
        if not isinstance(self.str_properties, Unset):
            str_properties = self.str_properties

        date_properties: Union[Unset, List[str]] = UNSET
        if not isinstance(self.date_properties, Unset):
            date_properties = []
            for componentsschemas_an_array_of_date_item_data in self.date_properties:
                componentsschemas_an_array_of_date_item = componentsschemas_an_array_of_date_item_data.isoformat()
                date_properties.append(componentsschemas_an_array_of_date_item)

        datetime_properties: Union[Unset, List[str]] = UNSET
        if not isinstance(self.datetime_properties, Unset):
            datetime_properties = []
            for componentsschemas_an_array_of_date_time_item_data in self.datetime_properties:
                componentsschemas_an_array_of_date_time_item = (
                    componentsschemas_an_array_of_date_time_item_data.isoformat()
                )

                datetime_properties.append(componentsschemas_an_array_of_date_time_item)

        int_32_properties: Union[Unset, List[int]] = UNSET
        if not isinstance(self.int_32_properties, Unset):
            int_32_properties = self.int_32_properties

        int_64_properties: Union[Unset, List[int]] = UNSET
        if not isinstance(self.int_64_properties, Unset):
            int_64_properties = self.int_64_properties

        float_properties: Union[Unset, List[float]] = UNSET
        if not isinstance(self.float_properties, Unset):
            float_properties = self.float_properties

        double_properties: Union[Unset, List[float]] = UNSET
        if not isinstance(self.double_properties, Unset):
            double_properties = self.double_properties

        file_properties: Union[Unset, List[Tuple[Optional[str], Union[BinaryIO, TextIO], Optional[str]]]] = UNSET
        if not isinstance(self.file_properties, Unset):
            file_properties = []
            for componentsschemas_an_array_of_file_item_data in self.file_properties:
                componentsschemas_an_array_of_file_item = componentsschemas_an_array_of_file_item_data.to_tuple()

                file_properties.append(componentsschemas_an_array_of_file_item)

        bytestream_properties: Union[Unset, List[str]] = UNSET
        if not isinstance(self.bytestream_properties, Unset):
            bytestream_properties = self.bytestream_properties

        enum_property_ref: Union[Unset, str] = UNSET
        if not isinstance(self.enum_property_ref, Unset):
            enum_property_ref = self.enum_property_ref.value

        str_property_ref = self.str_property_ref
        date_property_ref: Union[Unset, str] = UNSET
        if not isinstance(self.date_property_ref, Unset):
            date_property_ref = self.date_property_ref.isoformat()

        datetime_property_ref: Union[Unset, str] = UNSET
        if not isinstance(self.datetime_property_ref, Unset):
            datetime_property_ref = self.datetime_property_ref.isoformat()

        int_32_property_ref = self.int_32_property_ref
        int_64_property_ref = self.int_64_property_ref
        float_property_ref = self.float_property_ref
        double_property_ref = self.double_property_ref
        file_property_ref: Union[Unset, Tuple[Optional[str], Union[BinaryIO, TextIO], Optional[str]]] = UNSET
        if not isinstance(self.file_property_ref, Unset):
            file_property_ref = self.file_property_ref.to_tuple()

        bytestream_property_ref = self.bytestream_property_ref

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if enum_properties_ref is not UNSET:
            field_dict["enum_properties_ref"] = enum_properties_ref
        if str_properties_ref is not UNSET:
            field_dict["str_properties_ref"] = str_properties_ref
        if date_properties_ref is not UNSET:
            field_dict["date_properties_ref"] = date_properties_ref
        if datetime_properties_ref is not UNSET:
            field_dict["datetime_properties_ref"] = datetime_properties_ref
        if int_32_properties_ref is not UNSET:
            field_dict["int32_properties_ref"] = int_32_properties_ref
        if int_64_properties_ref is not UNSET:
            field_dict["int64_properties_ref"] = int_64_properties_ref
        if float_properties_ref is not UNSET:
            field_dict["float_properties_ref"] = float_properties_ref
        if double_properties_ref is not UNSET:
            field_dict["double_properties_ref"] = double_properties_ref
        if file_properties_ref is not UNSET:
            field_dict["file_properties_ref"] = file_properties_ref
        if bytestream_properties_ref is not UNSET:
            field_dict["bytestream_properties_ref"] = bytestream_properties_ref
        if enum_properties is not UNSET:
            field_dict["enum_properties"] = enum_properties
        if str_properties is not UNSET:
            field_dict["str_properties"] = str_properties
        if date_properties is not UNSET:
            field_dict["date_properties"] = date_properties
        if datetime_properties is not UNSET:
            field_dict["datetime_properties"] = datetime_properties
        if int_32_properties is not UNSET:
            field_dict["int32_properties"] = int_32_properties
        if int_64_properties is not UNSET:
            field_dict["int64_properties"] = int_64_properties
        if float_properties is not UNSET:
            field_dict["float_properties"] = float_properties
        if double_properties is not UNSET:
            field_dict["double_properties"] = double_properties
        if file_properties is not UNSET:
            field_dict["file_properties"] = file_properties
        if bytestream_properties is not UNSET:
            field_dict["bytestream_properties"] = bytestream_properties
        if enum_property_ref is not UNSET:
            field_dict["enum_property_ref"] = enum_property_ref
        if str_property_ref is not UNSET:
            field_dict["str_property_ref"] = str_property_ref
        if date_property_ref is not UNSET:
            field_dict["date_property_ref"] = date_property_ref
        if datetime_property_ref is not UNSET:
            field_dict["datetime_property_ref"] = datetime_property_ref
        if int_32_property_ref is not UNSET:
            field_dict["int32_property_ref"] = int_32_property_ref
        if int_64_property_ref is not UNSET:
            field_dict["int64_property_ref"] = int_64_property_ref
        if float_property_ref is not UNSET:
            field_dict["float_property_ref"] = float_property_ref
        if double_property_ref is not UNSET:
            field_dict["double_property_ref"] = double_property_ref
        if file_property_ref is not UNSET:
            field_dict["file_property_ref"] = file_property_ref
        if bytestream_property_ref is not UNSET:
            field_dict["bytestream_property_ref"] = bytestream_property_ref

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        enum_properties_ref = []
        _enum_properties_ref = d.pop("enum_properties_ref", UNSET)
        for componentsschemas_an_other_array_of_enum_item_data in _enum_properties_ref or []:
            componentsschemas_an_other_array_of_enum_item = AnEnum(componentsschemas_an_other_array_of_enum_item_data)

            enum_properties_ref.append(componentsschemas_an_other_array_of_enum_item)

        str_properties_ref = cast(List[str], d.pop("str_properties_ref", UNSET))

        date_properties_ref = []
        _date_properties_ref = d.pop("date_properties_ref", UNSET)
        for componentsschemas_an_other_array_of_date_item_data in _date_properties_ref or []:
            componentsschemas_an_other_array_of_date_item = isoparse(
                componentsschemas_an_other_array_of_date_item_data
            ).date()

            date_properties_ref.append(componentsschemas_an_other_array_of_date_item)

        datetime_properties_ref = []
        _datetime_properties_ref = d.pop("datetime_properties_ref", UNSET)
        for componentsschemas_an_other_array_of_date_time_item_data in _datetime_properties_ref or []:
            componentsschemas_an_other_array_of_date_time_item = isoparse(
                componentsschemas_an_other_array_of_date_time_item_data
            )

            datetime_properties_ref.append(componentsschemas_an_other_array_of_date_time_item)

        int_32_properties_ref = cast(List[int], d.pop("int32_properties_ref", UNSET))

        int_64_properties_ref = cast(List[int], d.pop("int64_properties_ref", UNSET))

        float_properties_ref = cast(List[float], d.pop("float_properties_ref", UNSET))

        double_properties_ref = cast(List[float], d.pop("double_properties_ref", UNSET))

        file_properties_ref = []
        _file_properties_ref = d.pop("file_properties_ref", UNSET)
        for componentsschemas_an_other_array_of_file_item_data in _file_properties_ref or []:
            componentsschemas_an_other_array_of_file_item = File(
                payload=BytesIO(componentsschemas_an_other_array_of_file_item_data)
            )

            file_properties_ref.append(componentsschemas_an_other_array_of_file_item)

        bytestream_properties_ref = cast(List[str], d.pop("bytestream_properties_ref", UNSET))

        enum_properties = []
        _enum_properties = d.pop("enum_properties", UNSET)
        for componentsschemas_an_array_of_enum_item_data in _enum_properties or []:
            componentsschemas_an_array_of_enum_item = AnEnum(componentsschemas_an_array_of_enum_item_data)

            enum_properties.append(componentsschemas_an_array_of_enum_item)

        str_properties = cast(List[str], d.pop("str_properties", UNSET))

        date_properties = []
        _date_properties = d.pop("date_properties", UNSET)
        for componentsschemas_an_array_of_date_item_data in _date_properties or []:
            componentsschemas_an_array_of_date_item = isoparse(componentsschemas_an_array_of_date_item_data).date()

            date_properties.append(componentsschemas_an_array_of_date_item)

        datetime_properties = []
        _datetime_properties = d.pop("datetime_properties", UNSET)
        for componentsschemas_an_array_of_date_time_item_data in _datetime_properties or []:
            componentsschemas_an_array_of_date_time_item = isoparse(componentsschemas_an_array_of_date_time_item_data)

            datetime_properties.append(componentsschemas_an_array_of_date_time_item)

        int_32_properties = cast(List[int], d.pop("int32_properties", UNSET))

        int_64_properties = cast(List[int], d.pop("int64_properties", UNSET))

        float_properties = cast(List[float], d.pop("float_properties", UNSET))

        double_properties = cast(List[float], d.pop("double_properties", UNSET))

        file_properties = []
        _file_properties = d.pop("file_properties", UNSET)
        for componentsschemas_an_array_of_file_item_data in _file_properties or []:
            componentsschemas_an_array_of_file_item = File(
                payload=BytesIO(componentsschemas_an_array_of_file_item_data)
            )

            file_properties.append(componentsschemas_an_array_of_file_item)

        bytestream_properties = cast(List[str], d.pop("bytestream_properties", UNSET))

        enum_property_ref: Union[Unset, AnEnum] = UNSET
        _enum_property_ref = d.pop("enum_property_ref", UNSET)
        if not isinstance(_enum_property_ref, Unset):
            enum_property_ref = AnEnum(_enum_property_ref)

        str_property_ref = d.pop("str_property_ref", UNSET)

        date_property_ref: Union[Unset, datetime.date] = UNSET
        _date_property_ref = d.pop("date_property_ref", UNSET)
        if not isinstance(_date_property_ref, Unset):
            date_property_ref = isoparse(_date_property_ref).date()

        datetime_property_ref: Union[Unset, datetime.datetime] = UNSET
        _datetime_property_ref = d.pop("datetime_property_ref", UNSET)
        if not isinstance(_datetime_property_ref, Unset):
            datetime_property_ref = isoparse(_datetime_property_ref)

        int_32_property_ref = d.pop("int32_property_ref", UNSET)

        int_64_property_ref = d.pop("int64_property_ref", UNSET)

        float_property_ref = d.pop("float_property_ref", UNSET)

        double_property_ref = d.pop("double_property_ref", UNSET)

        file_property_ref: Union[Unset, File] = UNSET
        _file_property_ref = d.pop("file_property_ref", UNSET)
        if not isinstance(_file_property_ref, Unset):
            file_property_ref = File(payload=BytesIO(_file_property_ref))

        bytestream_property_ref = d.pop("bytestream_property_ref", UNSET)

        a_model_with_properties_reference_that_are_not_object = cls(
            enum_properties_ref=enum_properties_ref,
            str_properties_ref=str_properties_ref,
            date_properties_ref=date_properties_ref,
            datetime_properties_ref=datetime_properties_ref,
            int_32_properties_ref=int_32_properties_ref,
            int_64_properties_ref=int_64_properties_ref,
            float_properties_ref=float_properties_ref,
            double_properties_ref=double_properties_ref,
            file_properties_ref=file_properties_ref,
            bytestream_properties_ref=bytestream_properties_ref,
            enum_properties=enum_properties,
            str_properties=str_properties,
            date_properties=date_properties,
            datetime_properties=datetime_properties,
            int_32_properties=int_32_properties,
            int_64_properties=int_64_properties,
            float_properties=float_properties,
            double_properties=double_properties,
            file_properties=file_properties,
            bytestream_properties=bytestream_properties,
            enum_property_ref=enum_property_ref,
            str_property_ref=str_property_ref,
            date_property_ref=date_property_ref,
            datetime_property_ref=datetime_property_ref,
            int_32_property_ref=int_32_property_ref,
            int_64_property_ref=int_64_property_ref,
            float_property_ref=float_property_ref,
            double_property_ref=double_property_ref,
            file_property_ref=file_property_ref,
            bytestream_property_ref=bytestream_property_ref,
        )

        a_model_with_properties_reference_that_are_not_object.additional_properties = d
        return a_model_with_properties_reference_that_are_not_object

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
