from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.status_code_patterns_response_2xx_status import StatusCodePatternsResponse2XXStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="StatusCodePatternsResponse2XX")


@_attrs_define
class StatusCodePatternsResponse2XX:
    """
    Attributes:
        status (Union[Unset, StatusCodePatternsResponse2XXStatus]):
    """

    status: Union[Unset, StatusCodePatternsResponse2XXStatus] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _status = d.pop("status", UNSET)
        status: Union[Unset, StatusCodePatternsResponse2XXStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = StatusCodePatternsResponse2XXStatus(_status)

        status_code_patterns_response_2xx = cls(
            status=status,
        )

        status_code_patterns_response_2xx.additional_properties = d
        return status_code_patterns_response_2xx

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
