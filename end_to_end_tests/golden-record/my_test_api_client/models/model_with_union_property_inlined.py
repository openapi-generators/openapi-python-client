from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.model_with_union_property_inlined_fruit_type_0 import ModelWithUnionPropertyInlinedFruitType0
from ..models.model_with_union_property_inlined_fruit_type_1 import ModelWithUnionPropertyInlinedFruitType1
from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelWithUnionPropertyInlined")


@attr.s(auto_attribs=True)
class ModelWithUnionPropertyInlined:
    """ """

    fruit: Union[ModelWithUnionPropertyInlinedFruitType0, ModelWithUnionPropertyInlinedFruitType1, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        fruit: Union[Dict[str, Any], Unset]
        if isinstance(self.fruit, Unset):
            fruit = UNSET
        elif isinstance(self.fruit, ModelWithUnionPropertyInlinedFruitType0):
            fruit = UNSET
            if not isinstance(self.fruit, Unset):
                fruit = self.fruit.to_dict()

        else:
            fruit = UNSET
            if not isinstance(self.fruit, Unset):
                fruit = self.fruit.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if fruit is not UNSET:
            field_dict["fruit"] = fruit

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_fruit(
            data: object,
        ) -> Union[ModelWithUnionPropertyInlinedFruitType0, ModelWithUnionPropertyInlinedFruitType1, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _fruit_type_0 = data
                fruit_type_0: Union[Unset, ModelWithUnionPropertyInlinedFruitType0]
                if isinstance(_fruit_type_0, Unset):
                    fruit_type_0 = UNSET
                else:
                    fruit_type_0 = ModelWithUnionPropertyInlinedFruitType0.from_dict(_fruit_type_0)

                return fruit_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            _fruit_type_1 = data
            fruit_type_1: Union[Unset, ModelWithUnionPropertyInlinedFruitType1]
            if isinstance(_fruit_type_1, Unset):
                fruit_type_1 = UNSET
            else:
                fruit_type_1 = ModelWithUnionPropertyInlinedFruitType1.from_dict(_fruit_type_1)

            return fruit_type_1

        fruit = _parse_fruit(d.pop("fruit", UNSET))

        model_with_union_property_inlined = cls(
            fruit=fruit,
        )

        return model_with_union_property_inlined
