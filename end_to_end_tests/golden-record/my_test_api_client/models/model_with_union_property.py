from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..models.an_enum import AnEnum
from ..models.an_int_enum import AnIntEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelWithUnionProperty")


@_attrs_define
class ModelWithUnionProperty:
    """
    Attributes:
        a_property (Union[AnEnum, AnIntEnum, Unset]):
    """

    a_property: Union[AnEnum, AnIntEnum, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        prop1: Union[Unset, int, str]
        if isinstance(self.a_property, Unset):
            prop1 = UNSET
        elif isinstance(self.a_property, AnEnum):
            prop1 = self.a_property.value
        else:
            prop1 = self.a_property.value

        field_dict: Dict[str, Any] = {}
        field_dict = {
            **field_dict,
            **({} if prop1 is UNSET else {"a_property": prop1}),
        }

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_a_property(data: object) -> Union[AnEnum, AnIntEnum, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                a_property_type_0 = AnEnum(data)

                return a_property_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, int):
                raise TypeError()
            a_property_type_1 = AnIntEnum(data)

            return a_property_type_1

        a_property = _parse_a_property(d.pop("a_property", UNSET))

        model_with_union_property = cls(
            a_property=a_property,
        )

        return model_with_union_property
