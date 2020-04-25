from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, cast

from .validation_error import ValidationError


@dataclass
class HTTPValidationError:
    """  """

    detail: Optional[List[ValidationError]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "detail": self.detail if self.detail is not None else None,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> HTTPValidationError:

        detail = []
        for detail_item in d.get("detail", []):
            detail.append(ValidationError.from_dict(detail_item))
        return HTTPValidationError(detail=detail,)
