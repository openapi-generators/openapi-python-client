from typing import Any, Dict, Type, TypeVar, Union, cast

import attr

from ..models.model_with_union_property_inlined_fruit_item0 import ModelWithUnionPropertyInlinedFruitItem0
from ..models.model_with_union_property_inlined_fruit_item1 import ModelWithUnionPropertyInlinedFruitItem1
from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelWithUnionPropertyInlined")


@attr.s(auto_attribs=True)
class ModelWithUnionPropertyInlined:
    """  """

    fruit: Union[Unset, ModelWithUnionPropertyInlinedFruitItem0, ModelWithUnionPropertyInlinedFruitItem1] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        fruit: Union[Unset, ModelWithUnionPropertyInlinedFruitItem0, ModelWithUnionPropertyInlinedFruitItem1]
        if isinstance(self.fruit, Unset):
            fruit = UNSET
        elif isinstance(self.fruit, ModelWithUnionPropertyInlinedFruitItem0):
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
            data: Any,
        ) -> Union[Unset, ModelWithUnionPropertyInlinedFruitItem0, ModelWithUnionPropertyInlinedFruitItem1]:
            data = None if isinstance(data, Unset) else data
            fruit: Union[Unset, ModelWithUnionPropertyInlinedFruitItem0, ModelWithUnionPropertyInlinedFruitItem1]
            try:
                _fruit_item0 = data
                if not isinstance(_fruit_item0, Unset):
                    ModelWithUnionPropertyInlinedFruitItem0.from_dict(cast(Dict[str, Any], _fruit_item0))

                return fruit
            except:  # noqa: E722
                pass
            _fruit_item1 = data
            if not isinstance(_fruit_item1, Unset):
                ModelWithUnionPropertyInlinedFruitItem1.from_dict(cast(Dict[str, Any], _fruit_item1))

            return fruit

        fruit = _parse_fruit(d.pop("fruit", UNSET))

        model_with_union_property_inlined = cls(
            fruit=fruit,
        )

        return model_with_union_property_inlined
