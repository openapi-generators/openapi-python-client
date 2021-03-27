from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelWithUnionProperty")


@attr.s(auto_attribs=True)
class ModelWithUnionProperty:
    """  """

    a_property: Union[None, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        a_property: Union[None, Unset]
        if isinstance(self.a_property, Unset):
            a_property = UNSET
        elif isinstance(self.a_property, None):
            a_property = None

        else:
            a_property = None

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if a_property is not UNSET:
            field_dict["a_property"] = a_property

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_a_property(data: object) -> Union[None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                a_property_type0: Union[Unset, None]
                if not data is None:
                    raise TypeError()
                a_property_type0 = UNSET

                return a_property_type0
            except:  # noqa: E722
                pass
            if not data is None:
                raise TypeError()
            a_property_type1: Union[Unset, None]
            a_property_type1 = UNSET

            return a_property_type1

        a_property = _parse_a_property(d.pop("a_property", UNSET))

        model_with_union_property = cls(
            a_property=a_property,
        )

        return model_with_union_property
