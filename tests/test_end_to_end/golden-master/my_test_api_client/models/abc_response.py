from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, cast


@dataclass
class ABCResponse:
    """  """

    success: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> ABCResponse:

        success = d["success"]

        return ABCResponse(success=success,)
