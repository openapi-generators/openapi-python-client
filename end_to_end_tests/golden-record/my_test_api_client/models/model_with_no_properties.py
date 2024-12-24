from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="ModelWithNoProperties")


@_attrs_define
class ModelWithNoProperties:
    """ """

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        model_with_no_properties = cls()

        return model_with_no_properties
