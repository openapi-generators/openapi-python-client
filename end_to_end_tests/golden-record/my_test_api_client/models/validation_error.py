from typing import Any, Dict, List, Optional, Set

import attr

from ..types import UNSET


@attr.s(auto_attribs=True)
class ValidationError:
    """  """

    loc: List[str]
    msg: str
    type: str

    def to_dict(
        self,
        include: Optional[Set[str]] = None,
        exclude: Optional[Set[str]] = None,
        exclude_unset: bool = False,
        exclude_none: bool = False,
    ) -> Dict[str, Any]:

        loc = self.loc

        msg = self.msg
        type = self.type

        all_properties = {
            "loc": loc,
            "msg": msg,
            "type": type,
        }

        trimmed_properties: Dict[str, Any] = {}
        for property_name, property_value in all_properties.items():
            if include is not None and property_name not in include:
                continue
            if exclude is not None and property_name in exclude:
                continue
            if exclude_unset and property_value is UNSET:
                continue
            if exclude_none and property_value is None:
                continue
            trimmed_properties[property_name] = property_value

        return trimmed_properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ValidationError":
        loc = d["loc"]

        msg = d["msg"]

        type = d["type"]

        return ValidationError(
            loc=loc,
            msg=msg,
            type=type,
        )
