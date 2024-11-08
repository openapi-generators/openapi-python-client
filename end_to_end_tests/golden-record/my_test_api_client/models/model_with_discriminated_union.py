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

        prop1: Union[Dict[str, Any], None, Unset]
        if isinstance(self.discriminated_union, Unset):
            prop1 = UNSET
        elif isinstance(self.discriminated_union, ADiscriminatedUnionType1):
            prop1 = self.discriminated_union.to_dict()
        elif isinstance(self.discriminated_union, ADiscriminatedUnionType2):
            prop1 = self.discriminated_union.to_dict()
        else:
            prop1 = self.discriminated_union

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict = {
            **field_dict,
            **({} if prop1 is UNSET else {"discriminated_union": prop1}),
        }

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
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_a_discriminated_union_type_0 = ADiscriminatedUnionType1.from_dict(data)

                return componentsschemas_a_discriminated_union_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_a_discriminated_union_type_1 = ADiscriminatedUnionType2.from_dict(data)

                return componentsschemas_a_discriminated_union_type_1
            except:  # noqa: E722
                pass
            return cast(Union["ADiscriminatedUnionType1", "ADiscriminatedUnionType2", None, Unset], data)

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
