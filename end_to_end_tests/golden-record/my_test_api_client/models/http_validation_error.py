from typing import Any, Dict, List, Optional, Set, cast

import attr

from ..models.validation_error import ValidationError
from ..types import UNSET


@attr.s(auto_attribs=True)
class HTTPValidationError:
    """  """

    detail: List[ValidationError] = cast(List[ValidationError], UNSET)

    def to_dict(
        self,
        include: Optional[Set[str]] = None,
        exclude: Optional[Set[str]] = None,
        exclude_unset: bool = False,
        exclude_none: bool = False,
    ) -> Dict[str, Any]:

        if self.detail is UNSET:
            detail = UNSET
        else:
            detail = []
            for detail_item_data in self.detail:
                detail_item = detail_item_data.to_dict(exclude_unset=True)

                detail.append(detail_item)

        all_properties = {
            "detail": detail,
        }

        trimmed_properties: Dict[str, Any] = {}
        for property_name, property_value in all_properties.items():
            if include is not None and property_name not in include:
                continue
            if exclude is not None and property_name in exclude:
                continue
            if exclude_unset and property_value is UNSET:
                continue
            if exclude_none and property_value is None:
                continue
            trimmed_properties[property_name] = property_value

        return trimmed_properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "HTTPValidationError":
        detail = []
        for detail_item_data in d.get("detail", UNSET) or []:
            detail_item = ValidationError.from_dict(detail_item_data)

            detail.append(detail_item)

        return HTTPValidationError(
            detail=detail,
        )
