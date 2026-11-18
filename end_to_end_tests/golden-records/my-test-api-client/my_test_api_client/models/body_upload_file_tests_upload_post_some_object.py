from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="BodyUploadFileTestsUploadPostSomeObject")


@_attrs_define
class BodyUploadFileTestsUploadPostSomeObject:
    """
    Attributes:
        num (float):
        text (str):
    """

    num: float
    text: str
    additional_properties: dict[str, Any] = _attrs_field(factory=dict)

    def to_dict(self) -> dict[str, Any]:
        num = self.num

        text = self.text

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "num": num,
                "text": text,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        num = d.pop("num")

        text = d.pop("text")

        return cls(
            num=num,
            text=text,
            additional_properties=d,
        )

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
