from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelWithRecursiveRef")


@_attrs_define
class ModelWithRecursiveRef:
    """
    Attributes:
        recursive (Union[Unset, ModelWithRecursiveRef]):
    """

    recursive: Union[Unset, "ModelWithRecursiveRef"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        prop1: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.recursive, Unset):
            prop1 = self.recursive.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict = {
            **field_dict,
            **({} if prop1 is UNSET else {"recursive": prop1}),
        }

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _recursive = d.pop("recursive", UNSET)
        recursive: Union[Unset, ModelWithRecursiveRef]
        if isinstance(_recursive, Unset):
            recursive = UNSET
        else:
            recursive = ModelWithRecursiveRef.from_dict(_recursive)

        model_with_recursive_ref = cls(
            recursive=recursive,
        )

        model_with_recursive_ref.additional_properties = d
        return model_with_recursive_ref

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
