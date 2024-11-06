from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

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
        discriminated_union (Union['ADiscriminatedUnionType1', 'ADiscriminatedUnionType2', None, Unset]):
    """

    discriminated_union: Union["ADiscriminatedUnionType1", "ADiscriminatedUnionType2", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.a_discriminated_union_type_1 import ADiscriminatedUnionType1
        from ..models.a_discriminated_union_type_2 import ADiscriminatedUnionType2

        discriminated_union: Union[Dict[str, Any], None, Unset]
        if isinstance(self.discriminated_union, Unset):
            discriminated_union = UNSET
        elif isinstance(self.discriminated_union, ADiscriminatedUnionType1):
            discriminated_union = self.discriminated_union.to_dict()
        elif isinstance(self.discriminated_union, ADiscriminatedUnionType2):
            discriminated_union = self.discriminated_union.to_dict()
        else:
            discriminated_union = self.discriminated_union

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if discriminated_union is not UNSET:
            field_dict["discriminated_union"] = discriminated_union

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.a_discriminated_union_type_1 import ADiscriminatedUnionType1
        from ..models.a_discriminated_union_type_2 import ADiscriminatedUnionType2

        d = src_dict.copy()

        def _parse_discriminated_union(
            data: object,
        ) -> Union["ADiscriminatedUnionType1", "ADiscriminatedUnionType2", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            if not isinstance(data, dict):
                raise TypeError()
            if "modelType" in data:
                _discriminator_value = data["modelType"]

                def _parse_1(data: object) -> ADiscriminatedUnionType1:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_a_discriminated_union_type_0 = ADiscriminatedUnionType1.from_dict(data)

                    return componentsschemas_a_discriminated_union_type_0

                def _parse_2(data: object) -> ADiscriminatedUnionType2:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_a_discriminated_union_type_1 = ADiscriminatedUnionType2.from_dict(data)

                    return componentsschemas_a_discriminated_union_type_1

                def _parse_3(data: object) -> ADiscriminatedUnionType2:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_a_discriminated_union_type_1 = ADiscriminatedUnionType2.from_dict(data)

                    return componentsschemas_a_discriminated_union_type_1

                _discriminator_mapping = {
                    "type1": _parse_1,
                    "type2": _parse_2,
                    "type2-another-value": _parse_3,
                }
                if _parse_fn := _discriminator_mapping.get(_discriminator_value):
                    return cast(
                        Union["ADiscriminatedUnionType1", "ADiscriminatedUnionType2", None, Unset], _parse_fn(data)
                    )
            raise TypeError("unrecognized value for property modelType")

        discriminated_union = _parse_discriminated_union(d.pop("discriminated_union", UNSET))

        model_with_discriminated_union = cls(
            discriminated_union=discriminated_union,
        )

        model_with_discriminated_union.additional_properties = d
        return model_with_discriminated_union

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
