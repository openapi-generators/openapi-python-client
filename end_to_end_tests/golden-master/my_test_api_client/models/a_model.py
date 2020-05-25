from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Dict, List, cast

from .an_enum_value import AnEnumValue
from .nested_list_of_enums_item_item import NestedListOfEnumsItemItem


@dataclass
class AModel:
    """ A Model for testing all the ways custom objects can be used  """

    an_enum_value: AnEnumValue
    nested_list_of_enums: List[List[NestedListOfEnumsItemItem]]
    a_camel_date_time: datetime
    a_date: date

    def to_dict(self) -> Dict[str, Any]:
        return {
            "an_enum_value": self.an_enum_value.value,
            "nested_list_of_enums": self.nested_list_of_enums,
            "aCamelDateTime": self.a_camel_date_time.isoformat(),
            "a_date": self.a_date.isoformat(),
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> AModel:
        an_enum_value = AnEnumValue(d["an_enum_value"])

        nested_list_of_enums = []
        for nested_list_of_enums_item_data in d["nested_list_of_enums"]:
            nested_list_of_enums_item = []
            for nested_list_of_enums_item_item_data in nested_list_of_enums_item_data:
                nested_list_of_enums_item_item = NestedListOfEnumsItemItem(nested_list_of_enums_item_item_data)

                nested_list_of_enums_item.append(nested_list_of_enums_item_item)

            nested_list_of_enums.append(nested_list_of_enums_item)

        a_camel_date_time = datetime.fromisoformat(d["aCamelDateTime"])

        a_date = date.fromisoformat(d["a_date"])

        return AModel(
            an_enum_value=an_enum_value,
            nested_list_of_enums=nested_list_of_enums,
            a_camel_date_time=a_camel_date_time,
            a_date=a_date,
        )
