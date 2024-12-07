from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.post_responses_unions_simple_before_complex_response_200a import (
        PostResponsesUnionsSimpleBeforeComplexResponse200A,
    )


T = TypeVar("T", bound="PostResponsesUnionsSimpleBeforeComplexResponse200")


@_attrs_define
class PostResponsesUnionsSimpleBeforeComplexResponse200:
    """
    Attributes:
        a (Union['PostResponsesUnionsSimpleBeforeComplexResponse200A', str]):
    """

    a: Union["PostResponsesUnionsSimpleBeforeComplexResponse200A", str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.post_responses_unions_simple_before_complex_response_200a import (
            PostResponsesUnionsSimpleBeforeComplexResponse200A,
        )

        a: Union[dict[str, Any], str]
        if isinstance(self.a, PostResponsesUnionsSimpleBeforeComplexResponse200A):
            a = self.a.to_dict()
        else:
            a = self.a

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "a": a,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.post_responses_unions_simple_before_complex_response_200a import (
            PostResponsesUnionsSimpleBeforeComplexResponse200A,
        )

        d = src_dict.copy()

        def _parse_a(data: object) -> Union["PostResponsesUnionsSimpleBeforeComplexResponse200A", str]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                a = PostResponsesUnionsSimpleBeforeComplexResponse200A.from_dict(data)

                return a
            except:  # noqa: E722
                pass
            return cast(Union["PostResponsesUnionsSimpleBeforeComplexResponse200A", str], data)

        a = _parse_a(d.pop("a"))

        post_responses_unions_simple_before_complex_response_200 = cls(
            a=a,
        )

        post_responses_unions_simple_before_complex_response_200.additional_properties = d
        return post_responses_unions_simple_before_complex_response_200

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
