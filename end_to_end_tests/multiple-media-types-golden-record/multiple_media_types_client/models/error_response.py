from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.error_response_detail import ErrorResponseDetail


T = TypeVar("T", bound="ErrorResponse")


@_attrs_define
class ErrorResponse:
    """
    Attributes:
        code (str): Error category code
        message (str): Human-readable error message
        detail (ErrorResponseDetail): Error detail
    """

    code: str
    message: str
    detail: "ErrorResponseDetail"

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        message = self.message

        detail = self.detail.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "code": code,
                "message": message,
                "detail": detail,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.error_response_detail import ErrorResponseDetail

        d = dict(src_dict)
        code = d.pop("code")

        message = d.pop("message")

        detail = ErrorResponseDetail.from_dict(d.pop("detail"))

        error_response = cls(
            code=code,
            message=message,
            detail=detail,
        )

        return error_response
