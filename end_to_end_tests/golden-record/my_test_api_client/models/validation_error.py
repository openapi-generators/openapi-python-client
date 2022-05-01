from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="ValidationError")


@attr.s(auto_attribs=True)
class ValidationError:
    """
    Attributes:
        location (List[str]):
        message (str):
        error_type (str):
    """

    location: List[str]
    message: str
    error_type: str

    def to_dict(self) -> Dict[str, Any]:
        location = self.location

        message = self.message
        error_type = self.error_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "loc": location,
                "msg": message,
                "type": error_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        location = cast(List[str], d.pop("loc"))

        message = d.pop("msg")

        error_type = d.pop("type")

        validation_error = cls(
            location=location,
            message=message,
            error_type=error_type,
        )

        return validation_error
