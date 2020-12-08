from typing import Any, Dict, List, Union

import attr

from ..models.validation_error import ValidationError
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class HTTPValidationError:
    """  """

    detail: Union[Unset, List[ValidationError]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        detail: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.detail, Unset):
            detail = []
            for detail_item_data in self.detail:
                detail_item = detail_item_data.to_dict()

                detail.append(detail_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if detail is not UNSET:
            field_dict["detail"] = detail

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "HTTPValidationError":
        d = src_dict.copy()
        detail = []
        _detail = d.pop("detail", UNSET)
        for detail_item_data in _detail or []:
            detail_item = ValidationError.from_dict(detail_item_data)

            detail.append(detail_item)

        http_validation_error = HTTPValidationError(
            detail=detail,
        )

        return http_validation_error
