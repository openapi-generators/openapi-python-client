from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class ValidationError:
    """  """

    loc: List[str]
    msg: str
    type: str

    def to_dict(self) -> Dict[str, Any]:
        loc = self.loc

        msg = self.msg
        type = self.type

        return {
            "loc": loc,
            "msg": msg,
            "type": type,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> ValidationError:
        loc = d["loc"]

        msg = d["msg"]

        type = d["type"]

        return ValidationError(loc=loc, msg=msg, type=type,)
