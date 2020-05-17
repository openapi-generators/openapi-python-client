from __future__ import annotations

from dataclasses import astuple, dataclass
from datetime import date, datetime
from typing import Any, Dict, List, Optional, cast

from .a_list_of_enums import AListOfEnums
from .an_enum_value import AnEnumValue
from .other_model import OtherModel
from .types import *


@dataclass
class AModel:
    """ A Model for testing all the ways custom objects can be used  """

    an_enum_value: AnEnumValue
    a_list_of_enums: List[AListOfEnums]
    a_list_of_strings: List[str]
    a_list_of_objects: List[OtherModel]
    a_camel_date_time: datetime
    a_date: date

    def to_dict(self) -> Dict[str, Any]:
        return {
            "an_enum_value": self.an_enum_value.value,
            "a_list_of_enums": self.a_list_of_enums,
            "a_list_of_strings": self.a_list_of_strings,
            "a_list_of_objects": self.a_list_of_objects,
            "aCamelDateTime": self.a_camel_date_time.isoformat(),
            "a_date": self.a_date.isoformat(),
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> AModel:

        an_enum_value = AnEnumValue(d["an_enum_value"])

        a_list_of_enums = []
        for a_list_of_enums_item in d.get("a_list_of_enums", []):
            a_list_of_enums.append(AListOfEnums(a_list_of_enums_item))

        a_list_of_strings = d.get("a_list_of_strings", [])

        a_list_of_objects = []
        for a_list_of_objects_item in d.get("a_list_of_objects", []):
            a_list_of_objects.append(OtherModel.from_dict(a_list_of_objects_item))

        a_camel_date_time = datetime.fromisoformat(d["aCamelDateTime"])

        a_date = date.fromisoformat(d["a_date"])

        return AModel(
            an_enum_value=an_enum_value,
            a_list_of_enums=a_list_of_enums,
            a_list_of_strings=a_list_of_strings,
            a_list_of_objects=a_list_of_objects,
            a_camel_date_time=a_camel_date_time,
            a_date=a_date,
        )
