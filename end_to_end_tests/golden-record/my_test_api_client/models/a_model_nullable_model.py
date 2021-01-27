from typing import Any, Dict, List, Union

import attr

from ..models.an_enum import AnEnum
from ..models.an_int_enum import AnIntEnum
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class AModelNullableModel:
    """  """

    a_property: Union[Unset, AnEnum, AnIntEnum] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

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
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if a_property is not UNSET:
            field_dict["a_property"] = a_property

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "AModelNullableModel":
        d = src_dict.copy()

        def _parse_a_property(data: Any) -> Union[Unset, AnEnum, AnIntEnum]:
            data = None if isinstance(data, Unset) else data
            a_property: Union[Unset, AnEnum, AnIntEnum]
            try:
                a_property = UNSET
                _a_property = data
                if _a_property is not None:
                    a_property = AnEnum(_a_property)

                return a_property
            except:  # noqa: E722
                pass
            a_property = UNSET
            _a_property = data
            if _a_property is not None:
                a_property = AnIntEnum(_a_property)

            return a_property

        a_property = _parse_a_property(d.pop("a_property", UNSET))

        a_model_nullable_model = AModelNullableModel(
            a_property=a_property,
        )

        a_model_nullable_model.additional_properties = d
        return a_model_nullable_model

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
