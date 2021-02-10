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
        a_property: Union[Unset, AnEnum, AnIntEnum]
        if isinstance(self.a_property, Unset):
            a_property = UNSET
        elif isinstance(self.a_property, AnEnum):
            a_property = UNSET
            if not isinstance(self.a_property, Unset):
                a_property = self.a_property

        else:
            a_property = UNSET
            if not isinstance(self.a_property, Unset):
                a_property = self.a_property

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if a_property is not UNSET:
            field_dict["a_property"] = a_property

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_a_property(data: Any) -> Union[Unset, AnEnum, AnIntEnum]:
            data = None if isinstance(data, Unset) else data
            try:
                a_property_item0: Union[Unset, AnEnum]
                a_property_item0 = UNSET
                _a_property_item0 = data
                if _a_property_item0 is not None and _a_property_item0 is not UNSET:
                    a_property_item0 = AnEnum(_a_property_item0)

                return a_property_item0
            except:  # noqa: E722
                pass
            a_property_item1: Union[Unset, AnIntEnum]
            a_property_item1 = UNSET
            _a_property_item1 = data
            if _a_property_item1 is not None and _a_property_item1 is not UNSET:
                a_property_item1 = AnIntEnum(_a_property_item1)

            return a_property_item1

        a_property = _parse_a_property(d.pop("a_property", UNSET))

        model_with_union_property = cls(
            a_property=a_property,
        )

        return model_with_union_property
