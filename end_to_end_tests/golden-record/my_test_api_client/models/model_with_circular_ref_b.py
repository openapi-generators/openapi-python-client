from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_with_circular_ref_a import ModelWithCircularRefA


T = TypeVar("T", bound="ModelWithCircularRefB")


@_attrs_define
class ModelWithCircularRefB:
    """
    Attributes:
        circular (Union[Unset, ModelWithCircularRefA]):
    """

    circular: Union[Unset, "ModelWithCircularRefA"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        circular: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.circular, Unset):
            circular = self.circular.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if circular is not UNSET:
            field_dict["circular"] = circular

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.model_with_circular_ref_a import ModelWithCircularRefA

        d = dict(src_dict)
        _circular = d.pop("circular", UNSET)
        circular: Union[Unset, ModelWithCircularRefA]
        if isinstance(_circular, Unset):
            circular = UNSET
        else:
            circular = ModelWithCircularRefA.from_dict(_circular)

        model_with_circular_ref_b = cls(
            circular=circular,
        )

        model_with_circular_ref_b.additional_properties = d
        return model_with_circular_ref_b

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
