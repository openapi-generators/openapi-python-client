from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, cast

from .a_list_of_enums import AListOfEnums
from .an_enum_value import AnEnumValue
from .other_model import OtherModel


@dataclass
class AModel:
    """ A Model for testing all the ways custom objects can be used  """

    an_enum_value: AnEnumValue
    a_list_of_enums: List[AListOfEnums]
    a_list_of_strings: List[str]
    a_list_of_objects: List[OtherModel]

    def to_dict(self) -> Dict:
        return {
            "an_enum_value": self.an_enum_value.value,
            "a_list_of_enums": self.a_list_of_enums,
            "a_list_of_strings": self.a_list_of_strings,
            "a_list_of_objects": self.a_list_of_objects,
        }

    @staticmethod
    def from_dict(d: Dict) -> AModel:

        an_enum_value = AnEnumValue(d["an_enum_value"]) if "an_enum_value" in d else None

        a_list_of_enums = []
        for a_list_of_enums_item in d.get("a_list_of_enums", []):
            a_list_of_enums.append(AListOfEnums(a_list_of_enums_item))

        a_list_of_strings = d.get("a_list_of_strings", [])

        a_list_of_objects = []
        for a_list_of_objects_item in d.get("a_list_of_objects", []):
            a_list_of_objects.append(OtherModel.from_dict(a_list_of_objects_item))
        return AModel(
            an_enum_value=an_enum_value,
            a_list_of_enums=a_list_of_enums,
            a_list_of_strings=a_list_of_strings,
            a_list_of_objects=a_list_of_objects,
        )
