from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..models.an_all_of_enum import AnAllOfEnum, check_an_all_of_enum
from ..models.an_enum import AnEnum, check_an_enum
from ..models.different_enum import DifferentEnum, check_different_enum
from ..types import UNSET, Unset

T = TypeVar("T", bound="AModel")


@_attrs_define
class AModel:
    """A Model for testing all the ways enums can be used

    Attributes:
        an_enum_value (AnEnum): For testing Enums in all the ways they can be used
        an_allof_enum_with_overridden_default (AnAllOfEnum):  Default: 'overridden_default'.
        any_value (Union[Unset, Any]):
        an_optional_allof_enum (Union[Unset, AnAllOfEnum]):
        nested_list_of_enums (Union[Unset, List[List[DifferentEnum]]]):
    """

    an_enum_value: AnEnum
    an_allof_enum_with_overridden_default: AnAllOfEnum = "overridden_default"
    any_value: Union[Unset, Any] = UNSET
    an_optional_allof_enum: Union[Unset, AnAllOfEnum] = UNSET
    nested_list_of_enums: Union[Unset, List[List[DifferentEnum]]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        prop1: str = self.an_enum_value
        prop2: str = self.an_allof_enum_with_overridden_default
        prop3 = self.any_value
        prop4: Union[Unset, str] = UNSET
        if not isinstance(self.an_optional_allof_enum, Unset):
            prop4 = self.an_optional_allof_enum

        prop5: Union[Unset, List[List[str]]] = UNSET
        if not isinstance(self.nested_list_of_enums, Unset):
            prop5 = []
            for nested_list_of_enums_item_data in self.nested_list_of_enums:
                nested_list_of_enums_item = []
                for nested_list_of_enums_item_item_data in nested_list_of_enums_item_data:
                    nested_list_of_enums_item_item: str = nested_list_of_enums_item_item_data
                    nested_list_of_enums_item.append(nested_list_of_enums_item_item)

                prop5.append(nested_list_of_enums_item)

        field_dict: Dict[str, Any] = {}
        field_dict = {
            **field_dict,
            "an_enum_value": prop1,
            "an_allof_enum_with_overridden_default": prop2,
            **({} if prop3 is UNSET else {"any_value": prop3}),
            **({} if prop4 is UNSET else {"an_optional_allof_enum": prop4}),
            **({} if prop5 is UNSET else {"nested_list_of_enums": prop5}),
        }

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        an_enum_value = check_an_enum(d.pop("an_enum_value"))

        an_allof_enum_with_overridden_default = check_an_all_of_enum(d.pop("an_allof_enum_with_overridden_default"))

        any_value = d.pop("any_value", UNSET)

        _an_optional_allof_enum = d.pop("an_optional_allof_enum", UNSET)
        an_optional_allof_enum: Union[Unset, AnAllOfEnum]
        if isinstance(_an_optional_allof_enum, Unset):
            an_optional_allof_enum = UNSET
        else:
            an_optional_allof_enum = check_an_all_of_enum(_an_optional_allof_enum)

        nested_list_of_enums = []
        _nested_list_of_enums = d.pop("nested_list_of_enums", UNSET)
        for nested_list_of_enums_item_data in _nested_list_of_enums or []:
            nested_list_of_enums_item = []
            _nested_list_of_enums_item = nested_list_of_enums_item_data
            for nested_list_of_enums_item_item_data in _nested_list_of_enums_item:
                nested_list_of_enums_item_item = check_different_enum(nested_list_of_enums_item_item_data)

                nested_list_of_enums_item.append(nested_list_of_enums_item_item)

            nested_list_of_enums.append(nested_list_of_enums_item)

        a_model = cls(
            an_enum_value=an_enum_value,
            an_allof_enum_with_overridden_default=an_allof_enum_with_overridden_default,
            any_value=any_value,
            an_optional_allof_enum=an_optional_allof_enum,
            nested_list_of_enums=nested_list_of_enums,
        )

        return a_model
