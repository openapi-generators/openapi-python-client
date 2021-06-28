from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="BodyUploadFileTestsUploadPostSomeNullableObject")


@attr.s(auto_attribs=True)
class BodyUploadFileTestsUploadPostSomeNullableObject:
    """ """

    bar: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        bar = self.bar

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if bar is not UNSET:
            field_dict["bar"] = bar

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        bar = d.pop("bar", UNSET)

        body_upload_file_tests_upload_post_some_nullable_object = cls(
            bar=bar,
        )

        body_upload_file_tests_upload_post_some_nullable_object.additional_properties = d
        return body_upload_file_tests_upload_post_some_nullable_object

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
