from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, cast


@dataclass
class OtherModel:
    """ A different model for calling from TestModel  """

    a_value: str

    def to_dict(self) -> Dict:
        return {
            "a_value": self.a_value,
        }

    @staticmethod
    def from_dict(d: Dict) -> OtherModel:

        a_value = d["a_value"]

        return OtherModel(a_value=a_value,)
