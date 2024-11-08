import threading
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Thing")


@_attrs_define
class Thing:
    """
    Attributes:
        req_prop_1_read_write (str):
        req_prop_2_read_only (str):
        opt_prop_1_read_write (Union[Unset, str]):
        opt_prop_2_read_only (Union[Unset, str]):
    """

    req_prop_1_read_write: str
    req_prop_2_read_only: str
    opt_prop_1_read_write: Union[Unset, str] = UNSET
    opt_prop_2_read_only: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        serialization_context = threading.local.openapi_serialization_context or {}
        skip_read_only = serialization_context.get("request_body", False)
        prop1 = self.req_prop_1_read_write
        prop2 = self.req_prop_2_read_only
        prop3 = self.opt_prop_1_read_write
        prop4 = self.opt_prop_2_read_only

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict = {
            **field_dict,
            "reqProp1ReadWrite": prop1,
            **({} if skip_read_only else {"reqProp2ReadOnly": prop2}),
            **({} if prop3 is UNSET else {"optProp1ReadWrite": prop3}),
            **({} if prop4 is UNSET or skip_read_only else {"optProp2ReadOnly": prop4}),
        }

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        serialization_context = threading.local.openapi_serialization_context or {}
        skip_read_only = serialization_context.get("request_body", False)
        prop1 = (None, str(self.req_prop_1_read_write).encode(), "text/plain")

        prop2 = (None, str(self.req_prop_2_read_only).encode(), "text/plain")

        prop3 = (
            self.opt_prop_1_read_write
            if isinstance(self.opt_prop_1_read_write, Unset)
            else (None, str(self.opt_prop_1_read_write).encode(), "text/plain")
        )

        prop4 = (
            self.opt_prop_2_read_only
            if isinstance(self.opt_prop_2_read_only, Unset)
            else (None, str(self.opt_prop_2_read_only).encode(), "text/plain")
        )

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict = {
            **field_dict,
            "reqProp1ReadWrite": prop1,
            **({} if skip_read_only else {"reqProp2ReadOnly": prop2}),
            **({} if prop3 is UNSET else {"optProp1ReadWrite": prop3}),
            **({} if prop4 is UNSET or skip_read_only else {"optProp2ReadOnly": prop4}),
        }

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        req_prop_1_read_write = d.pop("reqProp1ReadWrite")

        req_prop_2_read_only = d.pop("reqProp2ReadOnly")

        opt_prop_1_read_write = d.pop("optProp1ReadWrite", UNSET)

        opt_prop_2_read_only = d.pop("optProp2ReadOnly", UNSET)

        thing = cls(
            req_prop_1_read_write=req_prop_1_read_write,
            req_prop_2_read_only=req_prop_2_read_only,
            opt_prop_1_read_write=opt_prop_1_read_write,
            opt_prop_2_read_only=opt_prop_2_read_only,
        )

        thing.additional_properties = d
        return thing

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
