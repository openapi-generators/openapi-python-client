from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define, field

if TYPE_CHECKING:
    from ..models.post_responses_unions_simple_before_complex_response_200a_type_1 import (
        PostResponsesUnionsSimpleBeforeComplexResponse200AType1,
    )


T = TypeVar("T", bound="PostResponsesUnionsSimpleBeforeComplexResponse200")


@define
class PostResponsesUnionsSimpleBeforeComplexResponse200:
    """
    Attributes:
        a (Union['PostResponsesUnionsSimpleBeforeComplexResponse200AType1', str]):
    """

    a: Union["PostResponsesUnionsSimpleBeforeComplexResponse200AType1", str]
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.post_responses_unions_simple_before_complex_response_200a_type_1 import (
            PostResponsesUnionsSimpleBeforeComplexResponse200AType1,
        )

        a: Union[Dict[str, Any], str]

        if isinstance(self.a, PostResponsesUnionsSimpleBeforeComplexResponse200AType1):
            a = self.a.to_dict()

        else:
            a = self.a

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "a": a,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.post_responses_unions_simple_before_complex_response_200a_type_1 import (
            PostResponsesUnionsSimpleBeforeComplexResponse200AType1,
        )

        d = src_dict.copy()

        def _parse_a(data: object) -> Union["PostResponsesUnionsSimpleBeforeComplexResponse200AType1", str]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                a_type_1 = PostResponsesUnionsSimpleBeforeComplexResponse200AType1.from_dict(data)

                return a_type_1
            except:  # noqa: E722
                pass
            return cast(Union["PostResponsesUnionsSimpleBeforeComplexResponse200AType1", str], data)

        a = _parse_a(d.pop("a"))

        post_responses_unions_simple_before_complex_response_200 = cls(
            a=a,
        )

        post_responses_unions_simple_before_complex_response_200.additional_properties = d
        return post_responses_unions_simple_before_complex_response_200

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
