import datetime
from typing import Any, Dict, List, Optional, cast

import attr
from dateutil.parser import isoparse

from ..models.an_enum import AnEnum
from ..models.different_enum import DifferentEnum


@attr.s(auto_attribs=True)
class AModel:
    """ A Model for testing all the ways custom objects can be used  """

    an_enum_value: AnEnum
    some_dict: Optional[Dict[Any, Any]]
    a_camel_date_time: datetime.date
    a_date: datetime.date
    nested_list_of_enums: Optional[List[List[DifferentEnum]]] = None

    def to_dict(self) -> Dict[str, Any]:
        an_enum_value = self.an_enum_value.value

        some_dict = self.some_dict

        a_camel_date_time = self.a_camel_date_time.isoformat()

        a_date = self.a_date.isoformat()

        if self.nested_list_of_enums is None:
            nested_list_of_enums = None
        else:
            nested_list_of_enums = []
            for nested_list_of_enums_item_data in self.nested_list_of_enums:
                nested_list_of_enums_item = []
                for nested_list_of_enums_item_item_data in nested_list_of_enums_item_data:
                    nested_list_of_enums_item_item = nested_list_of_enums_item_item_data.value

                    nested_list_of_enums_item.append(nested_list_of_enums_item_item)

                nested_list_of_enums.append(nested_list_of_enums_item)

        return {
            "an_enum_value": an_enum_value,
            "some_dict": some_dict,
            "aCamelDateTime": a_camel_date_time,
            "a_date": a_date,
            "nested_list_of_enums": nested_list_of_enums,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AModel":
        an_enum_value = AnEnum(d["an_enum_value"])

        some_dict = d["some_dict"]

        a_camel_date_time = isoparse(d["aCamelDateTime"]).date()

        a_date = isoparse(d["a_date"]).date()

        nested_list_of_enums = []
        for nested_list_of_enums_item_data in d.get("nested_list_of_enums") or []:
            nested_list_of_enums_item = []
            for nested_list_of_enums_item_item_data in nested_list_of_enums_item_data:
                nested_list_of_enums_item_item = DifferentEnum(nested_list_of_enums_item_item_data)

                nested_list_of_enums_item.append(nested_list_of_enums_item_item)

            nested_list_of_enums.append(nested_list_of_enums_item)

        return AModel(
            an_enum_value=an_enum_value,
            some_dict=some_dict,
            a_camel_date_time=a_camel_date_time,
            a_date=a_date,
            nested_list_of_enums=nested_list_of_enums,
        )
