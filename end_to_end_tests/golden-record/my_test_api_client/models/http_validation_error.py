from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.validation_error import ValidationError


T = TypeVar("T", bound="HTTPValidationError")


@_attrs_define
class HTTPValidationError:
    """
    Attributes:
        detail (Union[Unset, List['ValidationError']]):
    """

    detail: Union[Unset, List["ValidationError"]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        prop1: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.detail, Unset):
            prop1 = []
            for detail_item_data in self.detail:
                detail_item = detail_item_data.to_dict()
                prop1.append(detail_item)

        field_dict: Dict[str, Any] = {}
        field_dict = {
            **field_dict,
            **({} if prop1 is UNSET else {"detail": prop1}),
        }

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.validation_error import ValidationError

        d = src_dict.copy()
        detail = []
        _detail = d.pop("detail", UNSET)
        for detail_item_data in _detail or []:
            detail_item = ValidationError.from_dict(detail_item_data)

            detail.append(detail_item)

        http_validation_error = cls(
            detail=detail,
        )

        return http_validation_error
