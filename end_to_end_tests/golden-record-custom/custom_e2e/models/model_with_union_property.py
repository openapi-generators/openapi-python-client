from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.an_enum import AnEnum
from ..models.an_int_enum import AnIntEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelWithUnionProperty")


@attr.s(auto_attribs=True)
class ModelWithUnionProperty:
    """  """

    a_property: Union[Unset, AnEnum, AnIntEnum] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        a_property: Union[Unset, str, int]
        if isinstance(self.a_property, Unset):
            a_property = UNSET
        elif isinstance(self.a_property, AnEnum):
            a_property = UNSET
            if not isinstance(self.a_property, Unset):
                a_property = self.a_property.value

        else:
            a_property = UNSET
            if not isinstance(self.a_property, Unset):
                a_property = self.a_property.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if a_property is not UNSET:
            field_dict["a_property"] = a_property

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_a_property(data: object) -> Union[Unset, AnEnum, AnIntEnum]:
            a_property: Union[Unset, AnEnum, AnIntEnum]
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, int):
                    raise TypeError()
                a_property = UNSET
                _a_property = data
                if not isinstance(_a_property, Unset):
                    a_property = AnEnum(_a_property)

                return a_property
            except:  # noqa: E722
                pass
            if not isinstance(data, int):
                raise TypeError()
            a_property = UNSET
            _a_property = data
            if not isinstance(_a_property, Unset):
                a_property = AnIntEnum(_a_property)

            return a_property

        a_property = _parse_a_property(d.pop("a_property", UNSET))

        model_with_union_property = cls(
            a_property=a_property,
        )

        return model_with_union_property
