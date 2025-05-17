from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="ValidationError")


@_attrs_define
class ValidationError:
    """
    Attributes:
        loc (list[str]):
        msg (str):
        type_ (str):
    """

    loc: list[str]
    msg: str
    type_: str

    def to_dict(self) -> dict[str, Any]:
        loc = self.loc

        msg = self.msg

        type_ = self.type_

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "loc": loc,
                "msg": msg,
                "type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        loc = cast(list[str], d.pop("loc"))

        msg = d.pop("msg")

        type_ = d.pop("type")

        validation_error = cls(
            loc=loc,
            msg=msg,
            type_=type_,
        )

        return validation_error
