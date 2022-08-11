from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ObjectHistory")


@attr.s(auto_attribs=True)
class ObjectHistory:
    """
    Attributes:
        id (Union[Unset, int]):  Example: 1.
        username (Union[Unset, str]):  Example: admin.
        date (Union[Unset, str]):  Example: 2019-02-04T21:09:31.661Z.
        note (Union[Unset, str]):  Example: Sso settings update.
        details (Union[Unset, str]):  Example: Is SSO Enabled false\nSelected SSO Provider.
    """

    id: Union[Unset, int] = UNSET
    username: Union[Unset, str] = UNSET
    date: Union[Unset, str] = UNSET
    note: Union[Unset, str] = UNSET
    details: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        username = self.username
        date = self.date
        note = self.note
        details = self.details

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if username is not UNSET:
            field_dict["username"] = username
        if date is not UNSET:
            field_dict["date"] = date
        if note is not UNSET:
            field_dict["note"] = note
        if details is not UNSET:
            field_dict["details"] = details

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        username = d.pop("username", UNSET)

        date = d.pop("date", UNSET)

        note = d.pop("note", UNSET)

        details = d.pop("details", UNSET)

        object_history = cls(
            id=id,
            username=username,
            date=date,
            note=note,
            details=details,
        )

        object_history.additional_properties = d
        return object_history

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
