from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.a_discriminated_union_type_1 import ADiscriminatedUnionType1
    from ..models.a_discriminated_union_type_2 import ADiscriminatedUnionType2


T = TypeVar("T", bound="ModelWithDiscriminatedUnion")


@_attrs_define
class ModelWithDiscriminatedUnion:
    """
    Attributes:
        discriminated_union (ADiscriminatedUnionType1 | ADiscriminatedUnionType2 | None | Unset):
    """

    discriminated_union: ADiscriminatedUnionType1 | ADiscriminatedUnionType2 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.a_discriminated_union_type_1 import ADiscriminatedUnionType1
        from ..models.a_discriminated_union_type_2 import ADiscriminatedUnionType2

        discriminated_union: dict[str, Any] | None | Unset
        if isinstance(self.discriminated_union, Unset):
            discriminated_union = UNSET
        elif isinstance(self.discriminated_union, ADiscriminatedUnionType1):
            discriminated_union = self.discriminated_union.to_dict()
        elif isinstance(self.discriminated_union, ADiscriminatedUnionType2):
            discriminated_union = self.discriminated_union.to_dict()
        else:
            discriminated_union = self.discriminated_union

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if discriminated_union is not UNSET:
            field_dict["discriminated_union"] = discriminated_union

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.a_discriminated_union_type_1 import ADiscriminatedUnionType1
        from ..models.a_discriminated_union_type_2 import ADiscriminatedUnionType2

        d = dict(src_dict)

        def _parse_discriminated_union(
            data: object,
        ) -> ADiscriminatedUnionType1 | ADiscriminatedUnionType2 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_a_discriminated_union_type_0 = ADiscriminatedUnionType1.from_dict(data)

                return componentsschemas_a_discriminated_union_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_a_discriminated_union_type_1 = ADiscriminatedUnionType2.from_dict(data)

                return componentsschemas_a_discriminated_union_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ADiscriminatedUnionType1 | ADiscriminatedUnionType2 | None | Unset, data)

        discriminated_union = _parse_discriminated_union(d.pop("discriminated_union", UNSET))

        model_with_discriminated_union = cls(
            discriminated_union=discriminated_union,
        )

        model_with_discriminated_union.additional_properties = d
        return model_with_discriminated_union

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
