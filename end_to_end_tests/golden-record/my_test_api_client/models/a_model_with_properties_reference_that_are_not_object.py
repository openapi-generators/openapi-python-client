from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from pydantic import ConfigDict
from tandem_platform.schema.protected import BaseModel

from ..models.an_enum import AnEnum
from ..types import File

T = TypeVar("T", bound="AModelWithPropertiesReferenceThatAreNotObject")


class AModelWithPropertiesReferenceThatAreNotObject(BaseModel):
    """
    Attributes:
        enum_properties_ref (list[AnEnum]):
        str_properties_ref (list[str]):
        date_properties_ref (list[datetime.date]):
        datetime_properties_ref (list[datetime.datetime]):
        int32_properties_ref (list[int]):
        int64_properties_ref (list[int]):
        float_properties_ref (list[float]):
        double_properties_ref (list[float]):
        file_properties_ref (list[File]):
        bytestream_properties_ref (list[str]):
        enum_properties (list[AnEnum]):
        str_properties (list[str]):
        date_properties (list[datetime.date]):
        datetime_properties (list[datetime.datetime]):
        int32_properties (list[int]):
        int64_properties (list[int]):
        float_properties (list[float]):
        double_properties (list[float]):
        file_properties (list[File]):
        bytestream_properties (list[str]):
        enum_property_ref (AnEnum): For testing Enums in all the ways they can be used
        str_property_ref (str):
        date_property_ref (datetime.date):
        datetime_property_ref (datetime.datetime):
        int32_property_ref (int):
        int64_property_ref (int):
        float_property_ref (float):
        double_property_ref (float):
        file_property_ref (File):
        bytestream_property_ref (str):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    enum_properties_ref: list[AnEnum]
    str_properties_ref: list[str]
    date_properties_ref: list[datetime.date]
    datetime_properties_ref: list[datetime.datetime]
    int32_properties_ref: list[int]
    int64_properties_ref: list[int]
    float_properties_ref: list[float]
    double_properties_ref: list[float]
    file_properties_ref: list[File]
    bytestream_properties_ref: list[str]
    enum_properties: list[AnEnum]
    str_properties: list[str]
    date_properties: list[datetime.date]
    datetime_properties: list[datetime.datetime]
    int32_properties: list[int]
    int64_properties: list[int]
    float_properties: list[float]
    double_properties: list[float]
    file_properties: list[File]
    bytestream_properties: list[str]
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

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)
