from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_with_union_property_inlined_fruit_type_0 import ModelWithUnionPropertyInlinedFruitType0
    from ..models.model_with_union_property_inlined_fruit_type_1 import ModelWithUnionPropertyInlinedFruitType1


T = TypeVar("T", bound="ModelWithUnionPropertyInlined")


@_attrs_define
class ModelWithUnionPropertyInlined:
    """
    Attributes:
        fruit (Union['ModelWithUnionPropertyInlinedFruitType0', 'ModelWithUnionPropertyInlinedFruitType1', Unset]):
    """

    fruit: Union["ModelWithUnionPropertyInlinedFruitType0", "ModelWithUnionPropertyInlinedFruitType1", Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        from ..models.model_with_union_property_inlined_fruit_type_0 import ModelWithUnionPropertyInlinedFruitType0

        prop1: Union[Dict[str, Any], Unset]
        if isinstance(self.fruit, Unset):
            prop1 = UNSET
        elif isinstance(self.fruit, ModelWithUnionPropertyInlinedFruitType0):
            prop1 = self.fruit.to_dict()
        else:
            prop1 = self.fruit.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict = {
            **field_dict,
            **({} if prop1 is UNSET else {"fruit": prop1}),
        }

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_with_union_property_inlined_fruit_type_0 import ModelWithUnionPropertyInlinedFruitType0
        from ..models.model_with_union_property_inlined_fruit_type_1 import ModelWithUnionPropertyInlinedFruitType1

        d = src_dict.copy()

        def _parse_fruit(
            data: object,
        ) -> Union["ModelWithUnionPropertyInlinedFruitType0", "ModelWithUnionPropertyInlinedFruitType1", Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                fruit_type_0 = ModelWithUnionPropertyInlinedFruitType0.from_dict(data)

                return fruit_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            fruit_type_1 = ModelWithUnionPropertyInlinedFruitType1.from_dict(data)

            return fruit_type_1

        fruit = _parse_fruit(d.pop("fruit", UNSET))

        model_with_union_property_inlined = cls(
            fruit=fruit,
        )

        return model_with_union_property_inlined
