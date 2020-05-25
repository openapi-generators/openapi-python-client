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
        for detail_item_data in d.get("detail") or []:
            detail_item = ValidationError.from_dict(detail_item_data)

            detail.append(detail_item)

        return HTTPValidationError(detail=detail,)
