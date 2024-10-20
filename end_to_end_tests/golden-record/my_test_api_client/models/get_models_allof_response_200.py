from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.a_model import AModel
    from ..models.extended import Extended


T = TypeVar("T", bound="GetModelsAllofResponse200")


@_attrs_define
class GetModelsAllofResponse200:
    """
    Attributes:
        aliased (Union[Unset, AModel]): A Model for testing all the ways custom objects can be used
        extended (Union[Unset, Extended]):
        model (Union[Unset, AModel]): A Model for testing all the ways custom objects can be used
    """

    aliased: Union[Unset, "AModel"] = UNSET
    extended: Union[Unset, "Extended"] = UNSET
    model: Union[Unset, "AModel"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        aliased: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.aliased, Unset):
            aliased = self.aliased.to_dict()

        extended: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.extended, Unset):
            extended = self.extended.to_dict()

        model: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.model, Unset):
            model = self.model.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if aliased is not UNSET:
            field_dict["aliased"] = aliased
        if extended is not UNSET:
            field_dict["extended"] = extended
        if model is not UNSET:
            field_dict["model"] = model

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.a_model import AModel
        from ..models.extended import Extended

        d = src_dict.copy()
        _aliased = d.pop("aliased", UNSET)
        aliased: Union[Unset, AModel]
        if isinstance(_aliased, Unset):
            aliased = UNSET
        else:
            aliased = AModel.from_dict(_aliased)

        _extended = d.pop("extended", UNSET)
        extended: Union[Unset, Extended]
        if isinstance(_extended, Unset):
            extended = UNSET
        else:
            extended = Extended.from_dict(_extended)

        _model = d.pop("model", UNSET)
        model: Union[Unset, AModel]
        if isinstance(_model, Unset):
            model = UNSET
        else:
            model = AModel.from_dict(_model)

        get_models_allof_response_200 = cls(
            aliased=aliased,
            extended=extended,
            model=model,
        )

        get_models_allof_response_200.additional_properties = d
        return get_models_allof_response_200

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
