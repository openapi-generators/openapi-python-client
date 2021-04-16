from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="BodyUploadFileTestsUploadPostSomeObject")


@attr.s(auto_attribs=True)
class BodyUploadFileTestsUploadPostSomeObject:
    """  """

    num: float
    text: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        num = self.num
        text = self.text

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "num": num,
                "text": text,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        num = d.pop("num")

        text = d.pop("text")

        body_upload_file_tests_upload_post_some_object = cls(
            num=num,
            text=text,
        )

        body_upload_file_tests_upload_post_some_object.additional_properties = d
        return body_upload_file_tests_upload_post_some_object

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
