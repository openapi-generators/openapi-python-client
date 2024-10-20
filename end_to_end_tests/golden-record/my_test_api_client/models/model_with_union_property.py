from typing import Any, TypeVar, Union

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

    def to_dict(self) -> dict[str, Any]:
        a_property: Union[Unset, int, str]
        if isinstance(self.a_property, Unset):
            a_property = UNSET
        elif isinstance(self.a_property, AnEnum):
            a_property = self.a_property.value
        else:
            a_property = self.a_property.value

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if a_property is not UNSET:
            field_dict["a_property"] = a_property

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
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
