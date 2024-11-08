from typing import Any, Dict, List, Literal, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostConstPathBody")


@_attrs_define
class PostConstPathBody:
    """
    Attributes:
        required (Literal['this always goes in the body']):
        nullable (Union[Literal['this or null goes in the body'], None]):
        optional (Union[Literal['this sometimes goes in the body'], Unset]):
    """

    required: Literal["this always goes in the body"]
    nullable: Union[Literal["this or null goes in the body"], None]
    optional: Union[Literal["this sometimes goes in the body"], Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        prop1 = self.required
        prop2: Union[Literal["this or null goes in the body"], None]
        prop2 = self.nullable
        prop3 = self.optional

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict = {
            **field_dict,
            "required": prop1,
            "nullable": prop2,
            **({} if prop3 is UNSET else {"optional": prop3}),
        }

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        required = cast(Literal["this always goes in the body"], d.pop("required"))
        if required != "this always goes in the body":
            raise ValueError(f"required must match const 'this always goes in the body', got '{required}'")

        def _parse_nullable(data: object) -> Union[Literal["this or null goes in the body"], None]:
            if data is None:
                return data
            nullable_type_1 = cast(Literal["this or null goes in the body"], data)
            if nullable_type_1 != "this or null goes in the body":
                raise ValueError(
                    f"nullable_type_1 must match const 'this or null goes in the body', got '{nullable_type_1}'"
                )
            return nullable_type_1
            return cast(Union[Literal["this or null goes in the body"], None], data)

        nullable = _parse_nullable(d.pop("nullable"))

        optional = cast(Union[Literal["this sometimes goes in the body"], Unset], d.pop("optional", UNSET))
        if optional != "this sometimes goes in the body" and not isinstance(optional, Unset):
            raise ValueError(f"optional must match const 'this sometimes goes in the body', got '{optional}'")

        post_const_path_body = cls(
            required=required,
            nullable=nullable,
            optional=optional,
        )

        post_const_path_body.additional_properties = d
        return post_const_path_body

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
