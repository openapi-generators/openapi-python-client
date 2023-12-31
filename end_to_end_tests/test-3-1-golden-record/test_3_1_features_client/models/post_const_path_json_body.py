from typing import Any, Dict, List, Literal, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostConstPathJsonBody")


@_attrs_define
class PostConstPathJsonBody:
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
        required = self.required

        nullable: Union[Literal["this or null goes in the body"], None]
        nullable = self.nullable

        optional = self.optional

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "required": required,
                "nullable": nullable,
            }
        )
        if optional is not UNSET:
            field_dict["optional"] = optional

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        required = d.pop("required")

        def _parse_nullable(data: object) -> Union[Literal["this or null goes in the body"], None]:
            if data is None:
                return data
            return cast(Union[Literal["this or null goes in the body"], None], data)

        nullable = _parse_nullable(d.pop("nullable"))

        optional = d.pop("optional", UNSET)

        post_const_path_json_body = cls(
            required=required,
            nullable=nullable,
            optional=optional,
        )

        post_const_path_json_body.additional_properties = d
        return post_const_path_json_body

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
