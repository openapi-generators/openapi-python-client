from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.model_with_circular_ref_b import ModelWithCircularRefB
from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelWithCircularRefA")


@attr.s(auto_attribs=True)
class ModelWithCircularRefA:
    """
    Attributes:
        circular (Union[Unset, ModelWithCircularRefB]):
    """

    circular: Union[Unset, ModelWithCircularRefB] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        circular: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.circular, Unset):
            circular = self.circular.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if circular is not UNSET:
            field_dict["circular"] = circular

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _circular = d.pop("circular", UNSET)
        circular: Union[Unset, ModelWithCircularRefB]
        if isinstance(_circular, Unset):
            circular = UNSET
        else:
            circular = ModelWithCircularRefB.from_dict(_circular)

        model_with_circular_ref_a = cls(
            circular=circular,
        )

        model_with_circular_ref_a.additional_properties = d
        return model_with_circular_ref_a

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
