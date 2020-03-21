from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, cast



@dataclass
class PingResponse:
    """  """
    success: bool

    def to_dict(self) -> Dict:
        return {
            "success": self.success,
        }

    @staticmethod
    def from_dict(d: Dict) -> PingResponse:

        success = d["success"]
        return PingResponse(
            success=success,
        )