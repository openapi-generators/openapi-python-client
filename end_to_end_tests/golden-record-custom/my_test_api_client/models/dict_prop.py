from typing import Any, Dict

import attr


@attr.s(auto_attribs=True)
class DictProp:
    """  """

    def to_dict(self) -> Dict[str, Any]:

        field_dict = {}

        return field_dict

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "DictProp":
        return DictProp()
