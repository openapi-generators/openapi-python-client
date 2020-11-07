import datetime
from typing import Any, Dict, List, Optional, Union

import attr
from dateutil.parser import isoparse

from ..models.an_enum import AnEnum
from ..models.different_enum import DifferentEnum


@attr.s(auto_attribs=True)
class AModel:
    """ A Model for testing all the ways custom objects can be used  """

    an_enum_value: AnEnum
    a_camel_date_time: Union[datetime.datetime, datetime.date]
    a_date: datetime.date
    required_not_nullable: str
    nested_list_of_enums: List[List[DifferentEnum]]
    attr_1_leading_digit: str
    required_nullable: Optional[str]
    not_required_nullable: Optional[str]
    not_required_not_nullable: str

    def to_dict(self) -> Dict[str, Any]:
        an_enum_value = self.an_enum_value.value

        if isinstance(self.a_camel_date_time, datetime.datetime):
            a_camel_date_time = self.a_camel_date_time.isoformat()

        else:
            a_camel_date_time = self.a_camel_date_time.isoformat()

        a_date = self.a_date.isoformat()

        required_not_nullable = self.required_not_nullable
        nested_list_of_enums = []
        for nested_list_of_enums_item_data in self.nested_list_of_enums:
            nested_list_of_enums_item = []
            for nested_list_of_enums_item_item_data in nested_list_of_enums_item_data:
                nested_list_of_enums_item_item = nested_list_of_enums_item_item_data.value

                nested_list_of_enums_item.append(nested_list_of_enums_item_item)

            nested_list_of_enums.append(nested_list_of_enums_item)

        attr_1_leading_digit = self.attr_1_leading_digit
        required_nullable = self.required_nullable
        not_required_nullable = self.not_required_nullable
        not_required_not_nullable = self.not_required_not_nullable

        field_dict = {
            "an_enum_value": an_enum_value,
            "aCamelDateTime": a_camel_date_time,
            "a_date": a_date,
            "required_not_nullable": required_not_nullable,
            "nested_list_of_enums": nested_list_of_enums,
            "1_leading_digit": attr_1_leading_digit,
            "required_nullable": required_nullable,
            "not_required_nullable": not_required_nullable,
            "not_required_not_nullable": not_required_not_nullable,
        }

        return field_dict

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AModel":
        an_enum_value = AnEnum(d["an_enum_value"])

        def _parse_a_camel_date_time(data: Dict[str, Any]) -> Union[datetime.datetime, datetime.date]:
            a_camel_date_time: Union[datetime.datetime, datetime.date]
            try:
                a_camel_date_time = isoparse(d["aCamelDateTime"])

                return a_camel_date_time
            except:  # noqa: E722
                pass
            a_camel_date_time = isoparse(d["aCamelDateTime"]).date()

            return a_camel_date_time

        a_camel_date_time = _parse_a_camel_date_time(d["aCamelDateTime"])

        a_date = isoparse(d["a_date"]).date()

        required_not_nullable = d["required_not_nullable"]

        nested_list_of_enums = []
        for nested_list_of_enums_item_data in d["nested_list_of_enums"]:
            nested_list_of_enums_item = []
            for nested_list_of_enums_item_item_data in nested_list_of_enums_item_data:
                nested_list_of_enums_item_item = DifferentEnum(nested_list_of_enums_item_item_data)

                nested_list_of_enums_item.append(nested_list_of_enums_item_item)

            nested_list_of_enums.append(nested_list_of_enums_item)

        attr_1_leading_digit = d["1_leading_digit"]

        required_nullable = d["required_nullable"]

        not_required_nullable = d["not_required_nullable"]

        not_required_not_nullable = d["not_required_not_nullable"]

        return AModel(
            an_enum_value=an_enum_value,
            a_camel_date_time=a_camel_date_time,
            a_date=a_date,
            required_not_nullable=required_not_nullable,
            nested_list_of_enums=nested_list_of_enums,
            attr_1_leading_digit=attr_1_leading_digit,
            required_nullable=required_nullable,
            not_required_nullable=not_required_nullable,
            not_required_not_nullable=not_required_not_nullable,
        )
