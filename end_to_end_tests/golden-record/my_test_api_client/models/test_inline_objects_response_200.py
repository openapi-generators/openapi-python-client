from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="TestInlineObjectsResponse200")


@_attrs_define
class TestInlineObjectsResponse200:
    """
    Attributes:
        a_property (str | Unset):
    """

    a_property: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        a_property = self.a_property

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if a_property is not UNSET:
            field_dict["a_property"] = a_property

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        a_property = d.pop("a_property", UNSET)

        test_inline_objects_response_200 = cls(
            a_property=a_property,
        )

        return test_inline_objects_response_200
