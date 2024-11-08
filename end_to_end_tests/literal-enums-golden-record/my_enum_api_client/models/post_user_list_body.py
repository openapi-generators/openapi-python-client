import json
from typing import Any, Dict, List, Tuple, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.an_all_of_enum import AnAllOfEnum, check_an_all_of_enum
from ..models.an_enum import AnEnum, check_an_enum
from ..models.an_enum_with_null import AnEnumWithNull, check_an_enum_with_null
from ..models.different_enum import DifferentEnum, check_different_enum
from ..types import UNSET, Unset

T = TypeVar("T", bound="PostUserListBody")


@_attrs_define
class PostUserListBody:
    """
    Attributes:
        an_enum_value (Union[Unset, List[AnEnum]]):
        an_enum_value_with_null (Union[Unset, List[Union[AnEnumWithNull, None]]]):
        an_enum_value_with_only_null (Union[Unset, List[None]]):
        an_allof_enum_with_overridden_default (Union[Unset, AnAllOfEnum]):  Default: 'overridden_default'.
        an_optional_allof_enum (Union[Unset, AnAllOfEnum]):
        nested_list_of_enums (Union[Unset, List[List[DifferentEnum]]]):
    """

    an_enum_value: Union[Unset, List[AnEnum]] = UNSET
    an_enum_value_with_null: Union[Unset, List[Union[AnEnumWithNull, None]]] = UNSET
    an_enum_value_with_only_null: Union[Unset, List[None]] = UNSET
    an_allof_enum_with_overridden_default: Union[Unset, AnAllOfEnum] = "overridden_default"
    an_optional_allof_enum: Union[Unset, AnAllOfEnum] = UNSET
    nested_list_of_enums: Union[Unset, List[List[DifferentEnum]]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        prop1: Union[Unset, List[str]] = UNSET
        if not isinstance(self.an_enum_value, Unset):
            prop1 = []
            for an_enum_value_item_data in self.an_enum_value:
                an_enum_value_item: str = an_enum_value_item_data
                prop1.append(an_enum_value_item)

        prop2: Union[Unset, List[Union[None, str]]] = UNSET
        if not isinstance(self.an_enum_value_with_null, Unset):
            prop2 = []
            for an_enum_value_with_null_item_data in self.an_enum_value_with_null:
                an_enum_value_with_null_item: Union[None, str]
                if isinstance(an_enum_value_with_null_item_data, str):
                    an_enum_value_with_null_item = an_enum_value_with_null_item_data
                else:
                    an_enum_value_with_null_item = an_enum_value_with_null_item_data
                prop2.append(an_enum_value_with_null_item)

        prop3: Union[Unset, List[None]] = UNSET
        if not isinstance(self.an_enum_value_with_only_null, Unset):
            prop3 = self.an_enum_value_with_only_null

        prop4: Union[Unset, str] = UNSET
        if not isinstance(self.an_allof_enum_with_overridden_default, Unset):
            prop4 = self.an_allof_enum_with_overridden_default

        prop5: Union[Unset, str] = UNSET
        if not isinstance(self.an_optional_allof_enum, Unset):
            prop5 = self.an_optional_allof_enum

        prop6: Union[Unset, List[List[str]]] = UNSET
        if not isinstance(self.nested_list_of_enums, Unset):
            prop6 = []
            for nested_list_of_enums_item_data in self.nested_list_of_enums:
                nested_list_of_enums_item = []
                for nested_list_of_enums_item_item_data in nested_list_of_enums_item_data:
                    nested_list_of_enums_item_item: str = nested_list_of_enums_item_item_data
                    nested_list_of_enums_item.append(nested_list_of_enums_item_item)

                prop6.append(nested_list_of_enums_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict = {
            **field_dict,
            **({} if prop1 is UNSET else {"an_enum_value": prop1}),
            **({} if prop2 is UNSET else {"an_enum_value_with_null": prop2}),
            **({} if prop3 is UNSET else {"an_enum_value_with_only_null": prop3}),
            **({} if prop4 is UNSET else {"an_allof_enum_with_overridden_default": prop4}),
            **({} if prop5 is UNSET else {"an_optional_allof_enum": prop5}),
            **({} if prop6 is UNSET else {"nested_list_of_enums": prop6}),
        }

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        prop1: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.an_enum_value, Unset):
            _temp_prop1 = []
            for an_enum_value_item_data in self.an_enum_value:
                an_enum_value_item: str = an_enum_value_item_data
                _temp_prop1.append(an_enum_value_item)
            prop1 = (None, json.dumps(_temp_prop1).encode(), "application/json")

        prop2: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.an_enum_value_with_null, Unset):
            _temp_prop2 = []
            for an_enum_value_with_null_item_data in self.an_enum_value_with_null:
                an_enum_value_with_null_item: Union[None, str]
                if isinstance(an_enum_value_with_null_item_data, str):
                    an_enum_value_with_null_item = an_enum_value_with_null_item_data
                else:
                    an_enum_value_with_null_item = an_enum_value_with_null_item_data
                _temp_prop2.append(an_enum_value_with_null_item)
            prop2 = (None, json.dumps(_temp_prop2).encode(), "application/json")

        prop3: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.an_enum_value_with_only_null, Unset):
            _temp_prop3 = self.an_enum_value_with_only_null
            prop3 = (None, json.dumps(_temp_prop3).encode(), "application/json")

        prop4: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.an_allof_enum_with_overridden_default, Unset):
            prop4 = (None, str(self.an_allof_enum_with_overridden_default).encode(), "text/plain")

        prop5: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.an_optional_allof_enum, Unset):
            prop5 = (None, str(self.an_optional_allof_enum).encode(), "text/plain")

        prop6: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.nested_list_of_enums, Unset):
            _temp_prop6 = []
            for nested_list_of_enums_item_data in self.nested_list_of_enums:
                nested_list_of_enums_item = []
                for nested_list_of_enums_item_item_data in nested_list_of_enums_item_data:
                    nested_list_of_enums_item_item: str = nested_list_of_enums_item_item_data
                    nested_list_of_enums_item.append(nested_list_of_enums_item_item)

                _temp_prop6.append(nested_list_of_enums_item)
            prop6 = (None, json.dumps(_temp_prop6).encode(), "application/json")

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict = {
            **field_dict,
            **({} if prop1 is UNSET else {"an_enum_value": prop1}),
            **({} if prop2 is UNSET else {"an_enum_value_with_null": prop2}),
            **({} if prop3 is UNSET else {"an_enum_value_with_only_null": prop3}),
            **({} if prop4 is UNSET else {"an_allof_enum_with_overridden_default": prop4}),
            **({} if prop5 is UNSET else {"an_optional_allof_enum": prop5}),
            **({} if prop6 is UNSET else {"nested_list_of_enums": prop6}),
        }

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        an_enum_value = []
        _an_enum_value = d.pop("an_enum_value", UNSET)
        for an_enum_value_item_data in _an_enum_value or []:
            an_enum_value_item = check_an_enum(an_enum_value_item_data)

            an_enum_value.append(an_enum_value_item)

        an_enum_value_with_null = []
        _an_enum_value_with_null = d.pop("an_enum_value_with_null", UNSET)
        for an_enum_value_with_null_item_data in _an_enum_value_with_null or []:

            def _parse_an_enum_value_with_null_item(data: object) -> Union[AnEnumWithNull, None]:
                if data is None:
                    return data
                try:
                    if not isinstance(data, str):
                        raise TypeError()
                    componentsschemas_an_enum_with_null_type_1 = check_an_enum_with_null(data)

                    return componentsschemas_an_enum_with_null_type_1
                except:  # noqa: E722
                    pass
                return cast(Union[AnEnumWithNull, None], data)

            an_enum_value_with_null_item = _parse_an_enum_value_with_null_item(an_enum_value_with_null_item_data)

            an_enum_value_with_null.append(an_enum_value_with_null_item)

        an_enum_value_with_only_null = cast(List[None], d.pop("an_enum_value_with_only_null", UNSET))

        _an_allof_enum_with_overridden_default = d.pop("an_allof_enum_with_overridden_default", UNSET)
        an_allof_enum_with_overridden_default: Union[Unset, AnAllOfEnum]
        if isinstance(_an_allof_enum_with_overridden_default, Unset):
            an_allof_enum_with_overridden_default = UNSET
        else:
            an_allof_enum_with_overridden_default = check_an_all_of_enum(_an_allof_enum_with_overridden_default)

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

        post_user_list_body = cls(
            an_enum_value=an_enum_value,
            an_enum_value_with_null=an_enum_value_with_null,
            an_enum_value_with_only_null=an_enum_value_with_only_null,
            an_allof_enum_with_overridden_default=an_allof_enum_with_overridden_default,
            an_optional_allof_enum=an_optional_allof_enum,
            nested_list_of_enums=nested_list_of_enums,
        )

        post_user_list_body.additional_properties = d
        return post_user_list_body

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
