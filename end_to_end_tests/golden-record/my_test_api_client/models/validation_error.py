from typing import Any, Dict, List, cast

import attr


@attr.s(auto_attribs=True)
class ValidationError:
    """  """

    loc: List[str]
    msg: str
    type: str

    def to_dict(self) -> Dict[str, Any]:
        loc = self.loc

        msg = self.msg
        type = self.type

        field_dict = {
            "loc": loc,
            "msg": msg,
            "type": type,
        }

        return field_dict

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ValidationError":
        loc = cast(List[str], d["loc"])

        msg = d["msg"]

        type = d["type"]

        return ValidationError(
            loc=loc,
            msg=msg,
            type=type,
        )
