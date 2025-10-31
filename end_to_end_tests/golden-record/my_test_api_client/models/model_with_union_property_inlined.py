from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_with_union_property_inlined_apples import ModelWithUnionPropertyInlinedApples
    from ..models.model_with_union_property_inlined_bananas import ModelWithUnionPropertyInlinedBananas


T = TypeVar("T", bound="ModelWithUnionPropertyInlined")


@_attrs_define
class ModelWithUnionPropertyInlined:
    """
    Attributes:
        fruit (ModelWithUnionPropertyInlinedApples | ModelWithUnionPropertyInlinedBananas | Unset):
    """

    fruit: ModelWithUnionPropertyInlinedApples | ModelWithUnionPropertyInlinedBananas | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.model_with_union_property_inlined_apples import ModelWithUnionPropertyInlinedApples

        fruit: dict[str, Any] | Unset
        if isinstance(self.fruit, Unset):
            fruit = UNSET
        elif isinstance(self.fruit, ModelWithUnionPropertyInlinedApples):
            fruit = self.fruit.to_dict()
        else:
            fruit = self.fruit.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if fruit is not UNSET:
            field_dict["fruit"] = fruit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.model_with_union_property_inlined_apples import ModelWithUnionPropertyInlinedApples
        from ..models.model_with_union_property_inlined_bananas import ModelWithUnionPropertyInlinedBananas

        d = dict(src_dict)

        def _parse_fruit(
            data: object,
        ) -> ModelWithUnionPropertyInlinedApples | ModelWithUnionPropertyInlinedBananas | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                fruit_apples = ModelWithUnionPropertyInlinedApples.from_dict(data)

                return fruit_apples
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            fruit_bananas = ModelWithUnionPropertyInlinedBananas.from_dict(data)

            return fruit_bananas

        fruit = _parse_fruit(d.pop("fruit", UNSET))

        model_with_union_property_inlined = cls(
            fruit=fruit,
        )

        return model_with_union_property_inlined
