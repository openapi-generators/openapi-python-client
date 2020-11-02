import datetime
from typing import Any, Dict, List, Optional, Set, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.an_enum import AnEnum
from ..models.different_enum import DifferentEnum
from ..types import UNSET


@attr.s(auto_attribs=True)
class AModel:
    """ A Model for testing all the ways custom objects can be used  """

    an_enum_value: AnEnum
    a_camel_date_time: Union[datetime.datetime, datetime.date]
    a_date: datetime.date
    required_not_nullable: str
    nested_list_of_enums: List[List[DifferentEnum]] = cast(List[List[DifferentEnum]], UNSET)
    some_dict: Optional[Dict[Any, Any]] = None
    attr_1_leading_digit: str = cast(str, UNSET)
    required_nullable: Optional[str] = None
    not_required_nullable: Optional[str] = cast(Optional[str], UNSET)
    not_required_not_nullable: str = cast(str, UNSET)

    def to_dict(
        self,
        include: Optional[Set[str]] = None,
        exclude: Optional[Set[str]] = None,
        exclude_unset: bool = False,
        exclude_none: bool = False,
    ) -> Dict[str, Any]:
        an_enum_value = self.an_enum_value.value

        if isinstance(self.a_camel_date_time, datetime.datetime):
            a_camel_date_time = self.a_camel_date_time.isoformat()

        else:
            a_camel_date_time = self.a_camel_date_time.isoformat()

        a_date = self.a_date.isoformat()

        required_not_nullable = self.required_not_nullable

        if self.nested_list_of_enums is UNSET:
            nested_list_of_enums = UNSET
        else:
            nested_list_of_enums = []
            for nested_list_of_enums_item_data in self.nested_list_of_enums:

                nested_list_of_enums_item = []
                for nested_list_of_enums_item_item_data in nested_list_of_enums_item_data:
                    nested_list_of_enums_item_item = nested_list_of_enums_item_item_data.value

                    nested_list_of_enums_item.append(nested_list_of_enums_item_item)

                nested_list_of_enums.append(nested_list_of_enums_item)

        some_dict = self.some_dict if self.some_dict else None

        attr_1_leading_digit = self.attr_1_leading_digit
        required_nullable = self.required_nullable
        not_required_nullable = self.not_required_nullable
        not_required_not_nullable = self.not_required_not_nullable

        all_properties = {
            "an_enum_value": an_enum_value,
            "aCamelDateTime": a_camel_date_time,
            "a_date": a_date,
            "required_not_nullable": required_not_nullable,
            "nested_list_of_enums": nested_list_of_enums,
            "some_dict": some_dict,
            "1_leading_digit": attr_1_leading_digit,
            "required_nullable": required_nullable,
            "not_required_nullable": not_required_nullable,
            "not_required_not_nullable": not_required_not_nullable,
        }

        trimmed_properties: Dict[str, Any] = {}
        for property_name, property_value in all_properties.items():
            if include is not None and property_name not in include:
                continue
            if exclude is not None and property_name in exclude:
                continue
            if exclude_unset and property_value is UNSET:
                continue
            if exclude_none and property_value is None:
                continue
            trimmed_properties[property_name] = property_value

        return trimmed_properties

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
        for nested_list_of_enums_item_data in d.get("nested_list_of_enums", UNSET) or []:
            nested_list_of_enums_item = []
            for nested_list_of_enums_item_item_data in nested_list_of_enums_item_data:
                nested_list_of_enums_item_item = DifferentEnum(nested_list_of_enums_item_item_data)

                nested_list_of_enums_item.append(nested_list_of_enums_item_item)

            nested_list_of_enums.append(nested_list_of_enums_item)

        some_dict = d["some_dict"]

        attr_1_leading_digit = d.get("1_leading_digit", UNSET)

        required_nullable = d["required_nullable"]

        not_required_nullable = d.get("not_required_nullable", UNSET)

        not_required_not_nullable = d.get("not_required_not_nullable", UNSET)

        return AModel(
            an_enum_value=an_enum_value,
            a_camel_date_time=a_camel_date_time,
            a_date=a_date,
            required_not_nullable=required_not_nullable,
            nested_list_of_enums=nested_list_of_enums,
            some_dict=some_dict,
            attr_1_leading_digit=attr_1_leading_digit,
            required_nullable=required_nullable,
            not_required_nullable=not_required_nullable,
            not_required_not_nullable=not_required_not_nullable,
        )
