from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class Response_200:
    """  """

    a_property: str

    def to_dict(self) -> Dict[str, Any]:
        a_property = self.a_property

        field_dict = {
            "a_property": a_property,
        }

        return field_dict

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Response_200":
        a_property = d["a_property"]

        return Response_200(
            a_property=a_property,
        )
