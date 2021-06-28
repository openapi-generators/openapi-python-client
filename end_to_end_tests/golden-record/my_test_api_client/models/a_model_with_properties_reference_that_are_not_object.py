import datetime
from io import BytesIO
from typing import Any, Dict, List, Type, TypeVar, cast

import attr
from dateutil.parser import isoparse

from ..models.an_enum import AnEnum
from ..types import File

T = TypeVar("T", bound="AModelWithPropertiesReferenceThatAreNotObject")


@attr.s(auto_attribs=True)
class AModelWithPropertiesReferenceThatAreNotObject:
    """ """

    enum_properties_ref: List[AnEnum]
    str_properties_ref: List[str]
    date_properties_ref: List[datetime.date]
    datetime_properties_ref: List[datetime.datetime]
    int32_properties_ref: List[int]
    int64_properties_ref: List[int]
    float_properties_ref: List[float]
    double_properties_ref: List[float]
    file_properties_ref: List[File]
    bytestream_properties_ref: List[str]
    enum_properties: List[AnEnum]
    str_properties: List[str]
    date_properties: List[datetime.date]
    datetime_properties: List[datetime.datetime]
    int32_properties: List[int]
    int64_properties: List[int]
    float_properties: List[float]
    double_properties: List[float]
    file_properties: List[File]
    bytestream_properties: List[str]
    enum_property_ref: AnEnum
    str_property_ref: str
    date_property_ref: datetime.date
    datetime_property_ref: datetime.datetime
    int32_property_ref: int
    int64_property_ref: int
    float_property_ref: float
    double_property_ref: float
    file_property_ref: File
    bytestream_property_ref: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        enum_properties_ref = []
        for componentsschemas_an_other_array_of_enum_item_data in self.enum_properties_ref:
            componentsschemas_an_other_array_of_enum_item = componentsschemas_an_other_array_of_enum_item_data.value

            enum_properties_ref.append(componentsschemas_an_other_array_of_enum_item)

        str_properties_ref = self.str_properties_ref

        date_properties_ref = []
        for componentsschemas_an_other_array_of_date_item_data in self.date_properties_ref:
            componentsschemas_an_other_array_of_date_item = (
                componentsschemas_an_other_array_of_date_item_data.isoformat()
            )
            date_properties_ref.append(componentsschemas_an_other_array_of_date_item)

        datetime_properties_ref = []
        for componentsschemas_an_other_array_of_date_time_item_data in self.datetime_properties_ref:
            componentsschemas_an_other_array_of_date_time_item = (
                componentsschemas_an_other_array_of_date_time_item_data.isoformat()
            )

            datetime_properties_ref.append(componentsschemas_an_other_array_of_date_time_item)

        int32_properties_ref = self.int32_properties_ref

        int64_properties_ref = self.int64_properties_ref

        float_properties_ref = self.float_properties_ref

        double_properties_ref = self.double_properties_ref

        file_properties_ref = []
        for componentsschemas_an_other_array_of_file_item_data in self.file_properties_ref:
            componentsschemas_an_other_array_of_file_item = (
                componentsschemas_an_other_array_of_file_item_data.to_tuple()
            )

            file_properties_ref.append(componentsschemas_an_other_array_of_file_item)

        bytestream_properties_ref = self.bytestream_properties_ref

        enum_properties = []
        for componentsschemas_an_array_of_enum_item_data in self.enum_properties:
            componentsschemas_an_array_of_enum_item = componentsschemas_an_array_of_enum_item_data.value

            enum_properties.append(componentsschemas_an_array_of_enum_item)

        str_properties = self.str_properties

        date_properties = []
        for componentsschemas_an_array_of_date_item_data in self.date_properties:
            componentsschemas_an_array_of_date_item = componentsschemas_an_array_of_date_item_data.isoformat()
            date_properties.append(componentsschemas_an_array_of_date_item)

        datetime_properties = []
        for componentsschemas_an_array_of_date_time_item_data in self.datetime_properties:
            componentsschemas_an_array_of_date_time_item = componentsschemas_an_array_of_date_time_item_data.isoformat()

            datetime_properties.append(componentsschemas_an_array_of_date_time_item)

        int32_properties = self.int32_properties

        int64_properties = self.int64_properties

        float_properties = self.float_properties

        double_properties = self.double_properties

        file_properties = []
        for componentsschemas_an_array_of_file_item_data in self.file_properties:
            componentsschemas_an_array_of_file_item = componentsschemas_an_array_of_file_item_data.to_tuple()

            file_properties.append(componentsschemas_an_array_of_file_item)

        bytestream_properties = self.bytestream_properties

        enum_property_ref = self.enum_property_ref.value

        str_property_ref = self.str_property_ref
        date_property_ref = self.date_property_ref.isoformat()
        datetime_property_ref = self.datetime_property_ref.isoformat()

        int32_property_ref = self.int32_property_ref
        int64_property_ref = self.int64_property_ref
        float_property_ref = self.float_property_ref
        double_property_ref = self.double_property_ref
        file_property_ref = self.file_property_ref.to_tuple()

        bytestream_property_ref = self.bytestream_property_ref

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "enum_properties_ref": enum_properties_ref,
                "str_properties_ref": str_properties_ref,
                "date_properties_ref": date_properties_ref,
                "datetime_properties_ref": datetime_properties_ref,
                "int32_properties_ref": int32_properties_ref,
                "int64_properties_ref": int64_properties_ref,
                "float_properties_ref": float_properties_ref,
                "double_properties_ref": double_properties_ref,
                "file_properties_ref": file_properties_ref,
                "bytestream_properties_ref": bytestream_properties_ref,
                "enum_properties": enum_properties,
                "str_properties": str_properties,
                "date_properties": date_properties,
                "datetime_properties": datetime_properties,
                "int32_properties": int32_properties,
                "int64_properties": int64_properties,
                "float_properties": float_properties,
                "double_properties": double_properties,
                "file_properties": file_properties,
                "bytestream_properties": bytestream_properties,
                "enum_property_ref": enum_property_ref,
                "str_property_ref": str_property_ref,
                "date_property_ref": date_property_ref,
                "datetime_property_ref": datetime_property_ref,
                "int32_property_ref": int32_property_ref,
                "int64_property_ref": int64_property_ref,
                "float_property_ref": float_property_ref,
                "double_property_ref": double_property_ref,
                "file_property_ref": file_property_ref,
                "bytestream_property_ref": bytestream_property_ref,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        enum_properties_ref = []
        _enum_properties_ref = d.pop("enum_properties_ref")
        for componentsschemas_an_other_array_of_enum_item_data in _enum_properties_ref:
            componentsschemas_an_other_array_of_enum_item = AnEnum(componentsschemas_an_other_array_of_enum_item_data)

            enum_properties_ref.append(componentsschemas_an_other_array_of_enum_item)

        str_properties_ref = cast(List[str], d.pop("str_properties_ref"))

        date_properties_ref = []
        _date_properties_ref = d.pop("date_properties_ref")
        for componentsschemas_an_other_array_of_date_item_data in _date_properties_ref:
            componentsschemas_an_other_array_of_date_item = isoparse(
                componentsschemas_an_other_array_of_date_item_data
            ).date()

            date_properties_ref.append(componentsschemas_an_other_array_of_date_item)

        datetime_properties_ref = []
        _datetime_properties_ref = d.pop("datetime_properties_ref")
        for componentsschemas_an_other_array_of_date_time_item_data in _datetime_properties_ref:
            componentsschemas_an_other_array_of_date_time_item = isoparse(
                componentsschemas_an_other_array_of_date_time_item_data
            )

            datetime_properties_ref.append(componentsschemas_an_other_array_of_date_time_item)

        int32_properties_ref = cast(List[int], d.pop("int32_properties_ref"))

        int64_properties_ref = cast(List[int], d.pop("int64_properties_ref"))

        float_properties_ref = cast(List[float], d.pop("float_properties_ref"))

        double_properties_ref = cast(List[float], d.pop("double_properties_ref"))

        file_properties_ref = []
        _file_properties_ref = d.pop("file_properties_ref")
        for componentsschemas_an_other_array_of_file_item_data in _file_properties_ref:
            componentsschemas_an_other_array_of_file_item = File(
                payload=BytesIO(componentsschemas_an_other_array_of_file_item_data)
            )

            file_properties_ref.append(componentsschemas_an_other_array_of_file_item)

        bytestream_properties_ref = cast(List[str], d.pop("bytestream_properties_ref"))

        enum_properties = []
        _enum_properties = d.pop("enum_properties")
        for componentsschemas_an_array_of_enum_item_data in _enum_properties:
            componentsschemas_an_array_of_enum_item = AnEnum(componentsschemas_an_array_of_enum_item_data)

            enum_properties.append(componentsschemas_an_array_of_enum_item)

        str_properties = cast(List[str], d.pop("str_properties"))

        date_properties = []
        _date_properties = d.pop("date_properties")
        for componentsschemas_an_array_of_date_item_data in _date_properties:
            componentsschemas_an_array_of_date_item = isoparse(componentsschemas_an_array_of_date_item_data).date()

            date_properties.append(componentsschemas_an_array_of_date_item)

        datetime_properties = []
        _datetime_properties = d.pop("datetime_properties")
        for componentsschemas_an_array_of_date_time_item_data in _datetime_properties:
            componentsschemas_an_array_of_date_time_item = isoparse(componentsschemas_an_array_of_date_time_item_data)

            datetime_properties.append(componentsschemas_an_array_of_date_time_item)

        int32_properties = cast(List[int], d.pop("int32_properties"))

        int64_properties = cast(List[int], d.pop("int64_properties"))

        float_properties = cast(List[float], d.pop("float_properties"))

        double_properties = cast(List[float], d.pop("double_properties"))

        file_properties = []
        _file_properties = d.pop("file_properties")
        for componentsschemas_an_array_of_file_item_data in _file_properties:
            componentsschemas_an_array_of_file_item = File(
                payload=BytesIO(componentsschemas_an_array_of_file_item_data)
            )

            file_properties.append(componentsschemas_an_array_of_file_item)

        bytestream_properties = cast(List[str], d.pop("bytestream_properties"))

        enum_property_ref = AnEnum(d.pop("enum_property_ref"))

        str_property_ref = d.pop("str_property_ref")

        date_property_ref = isoparse(d.pop("date_property_ref")).date()

        datetime_property_ref = isoparse(d.pop("datetime_property_ref"))

        int32_property_ref = d.pop("int32_property_ref")

        int64_property_ref = d.pop("int64_property_ref")

        float_property_ref = d.pop("float_property_ref")

        double_property_ref = d.pop("double_property_ref")

        file_property_ref = File(payload=BytesIO(d.pop("file_property_ref")))

        bytestream_property_ref = d.pop("bytestream_property_ref")

        a_model_with_properties_reference_that_are_not_object = cls(
            enum_properties_ref=enum_properties_ref,
            str_properties_ref=str_properties_ref,
            date_properties_ref=date_properties_ref,
            datetime_properties_ref=datetime_properties_ref,
            int32_properties_ref=int32_properties_ref,
            int64_properties_ref=int64_properties_ref,
            float_properties_ref=float_properties_ref,
            double_properties_ref=double_properties_ref,
            file_properties_ref=file_properties_ref,
            bytestream_properties_ref=bytestream_properties_ref,
            enum_properties=enum_properties,
            str_properties=str_properties,
            date_properties=date_properties,
            datetime_properties=datetime_properties,
            int32_properties=int32_properties,
            int64_properties=int64_properties,
            float_properties=float_properties,
            double_properties=double_properties,
            file_properties=file_properties,
            bytestream_properties=bytestream_properties,
            enum_property_ref=enum_property_ref,
            str_property_ref=str_property_ref,
            date_property_ref=date_property_ref,
            datetime_property_ref=datetime_property_ref,
            int32_property_ref=int32_property_ref,
            int64_property_ref=int64_property_ref,
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
