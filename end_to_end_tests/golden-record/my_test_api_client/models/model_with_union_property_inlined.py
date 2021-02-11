from typing import Any, Dict, Type, TypeVar, Union

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
            try:
                fruit_item0: Union[ModelWithUnionPropertyInlinedFruitItem0, Unset]
                fruit_item0 = UNSET
                _fruit_item0 = data
                if not isinstance(_fruit_item0, Unset):
                    fruit_item0 = ModelWithUnionPropertyInlinedFruitItem0.from_dict(_fruit_item0)

                return fruit_item0
            except:  # noqa: E722
                pass
            fruit_item1: Union[ModelWithUnionPropertyInlinedFruitItem1, Unset]
            fruit_item1 = UNSET
            _fruit_item1 = data
            if not isinstance(_fruit_item1, Unset):
                fruit_item1 = ModelWithUnionPropertyInlinedFruitItem1.from_dict(_fruit_item1)

            return fruit_item1

        fruit = _parse_fruit(d.pop("fruit", UNSET))

        model_with_union_property_inlined = cls(
            fruit=fruit,
        )

        return model_with_union_property_inlined
