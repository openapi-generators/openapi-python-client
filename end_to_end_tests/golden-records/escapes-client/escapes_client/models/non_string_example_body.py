from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.non_string_example_body_dict_example import NonStringExampleBodyDictExample


T = TypeVar("T", bound="NonStringExampleBody")


@_attrs_define
class NonStringExampleBody:
    """
    Attributes:
        dict_example (NonStringExampleBodyDictExample | Unset):  Example: {'nested': 'dict example \"\"\" print(\\'uh
            oh\\')'}.
    """

    dict_example: NonStringExampleBodyDictExample | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        dict_example: dict[str, Any] | Unset = UNSET
        if not isinstance(self.dict_example, Unset):
            dict_example = self.dict_example.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if dict_example is not UNSET:
            field_dict["dict_example"] = dict_example

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.non_string_example_body_dict_example import NonStringExampleBodyDictExample  # noqa: PLC0415

        d = dict(src_dict)
        _dict_example = d.pop("dict_example", UNSET)
        dict_example: NonStringExampleBodyDictExample | Unset
        if isinstance(_dict_example, Unset):
            dict_example = UNSET
        else:
            dict_example = NonStringExampleBodyDictExample.from_dict(_dict_example)

        non_string_example_body = cls(
            dict_example=dict_example,
        )

        non_string_example_body.additional_properties = d
        return non_string_example_body

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
