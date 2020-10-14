from typing import Any, Dict, Optional

import attr


@attr.s(auto_attribs=True)
class JsonBody:
    """  """

    a_property: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        a_property = self.a_property

        return {
            "a_property": a_property,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "JsonBody":
        a_property = d.get("a_property")

        return JsonBody(
            a_property=a_property,
        )
