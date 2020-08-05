from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Union, cast

from .an_enum import AnEnum
from .different_enum import DifferentEnum


@dataclass
class AModel:
    """ A Model for testing all the ways custom objects can be used  """

    an_enum_value: AnEnum
    a_camel_date_time: Union[datetime, date]
    a_date: date
    nested_list_of_enums: Optional[List[List[DifferentEnum]]] = field(
        default_factory=lambda: cast(Optional[List[List[DifferentEnum]]], [])
    )
    some_dict: Optional[Dict[Any, Any]] = field(default_factory=lambda: cast(Optional[Dict[Any, Any]], {}))

    def to_dict(self) -> Dict[str, Any]:
        an_enum_value = self.an_enum_value.value

        if isinstance(self.a_camel_date_time, datetime):
            a_camel_date_time = self.a_camel_date_time.isoformat()

        else:
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

        some_dict = self.some_dict

        return {
            "an_enum_value": an_enum_value,
            "aCamelDateTime": a_camel_date_time,
            "a_date": a_date,
            "nested_list_of_enums": nested_list_of_enums,
            "some_dict": some_dict,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> AModel:
        an_enum_value = AnEnum(d["an_enum_value"])

        def _parse_a_camel_date_time(data: Dict[str, Any]) -> Union[datetime, date]:
            a_camel_date_time: Union[datetime, date]
            try:
                a_camel_date_time = datetime.fromisoformat(d["aCamelDateTime"])

                return a_camel_date_time
            except:
                pass
            a_camel_date_time = date.fromisoformat(d["aCamelDateTime"])

            return a_camel_date_time

        a_camel_date_time = _parse_a_camel_date_time(d["aCamelDateTime"])

        a_date = date.fromisoformat(d["a_date"])

        nested_list_of_enums = []
        for nested_list_of_enums_item_data in d.get("nested_list_of_enums") or []:
            nested_list_of_enums_item = []
            for nested_list_of_enums_item_item_data in nested_list_of_enums_item_data:
                nested_list_of_enums_item_item = DifferentEnum(nested_list_of_enums_item_item_data)

                nested_list_of_enums_item.append(nested_list_of_enums_item_item)

            nested_list_of_enums.append(nested_list_of_enums_item)

        some_dict = d.get("some_dict")

        return AModel(
            an_enum_value=an_enum_value,
            a_camel_date_time=a_camel_date_time,
            a_date=a_date,
            nested_list_of_enums=nested_list_of_enums,
            some_dict=some_dict,
        )
