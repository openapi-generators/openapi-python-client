from typing import Any, Dict, List

import attr

from ..models.validation_error import ValidationError


@attr.s(auto_attribs=True)
class HTTPValidationError:
    """  """

    detail: List[ValidationError]

    def to_dict(self) -> Dict[str, Any]:
        detail = []
        for detail_item_data in self.detail:
            detail_item = detail_item_data.to_dict()

            detail.append(detail_item)

        field_dict = {
            "detail": detail,
        }

        return field_dict

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "HTTPValidationError":
        detail = []
        for detail_item_data in d["detail"]:
            detail_item = ValidationError.from_dict(detail_item_data)

            detail.append(detail_item)

        return HTTPValidationError(
            detail=detail,
        )
