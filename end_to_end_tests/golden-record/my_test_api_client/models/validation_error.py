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

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "loc": loc,
                "msg": msg,
                "type": type,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "ValidationError":
        d = src_dict.copy()
        loc = cast(List[str], d.pop("loc"))

        msg = d.pop("msg")

        type = d.pop("type")

        validation_error = ValidationError(
            loc=loc,
            msg=msg,
            type=type,
        )

        return validation_error
