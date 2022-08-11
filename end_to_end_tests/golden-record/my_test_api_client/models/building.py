from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Building")


@attr.s(auto_attribs=True)
class Building:
    """
    Attributes:
        name (str):  Example: Apple Park.
        id (Union[Unset, str]):  Example: 1.
        street_address_1 (Union[Unset, None, str]):  Example: The McIntosh Tree.
        street_address_2 (Union[Unset, None, str]):  Example: One Apple Park Way.
        city (Union[Unset, None, str]):  Example: Cupertino.
        state_province (Union[Unset, None, str]):  Example: California.
        zip_postal_code (Union[Unset, None, str]):  Example: 95014.
        country (Union[Unset, None, str]):  Example: The United States of America.
    """

    name: str
    id: Union[Unset, str] = UNSET
    street_address_1: Union[Unset, None, str] = UNSET
    street_address_2: Union[Unset, None, str] = UNSET
    city: Union[Unset, None, str] = UNSET
    state_province: Union[Unset, None, str] = UNSET
    zip_postal_code: Union[Unset, None, str] = UNSET
    country: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        id = self.id
        street_address_1 = self.street_address_1
        street_address_2 = self.street_address_2
        city = self.city
        state_province = self.state_province
        zip_postal_code = self.zip_postal_code
        country = self.country

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if street_address_1 is not UNSET:
            field_dict["streetAddress1"] = street_address_1
        if street_address_2 is not UNSET:
            field_dict["streetAddress2"] = street_address_2
        if city is not UNSET:
            field_dict["city"] = city
        if state_province is not UNSET:
            field_dict["stateProvince"] = state_province
        if zip_postal_code is not UNSET:
            field_dict["zipPostalCode"] = zip_postal_code
        if country is not UNSET:
            field_dict["country"] = country

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        id = d.pop("id", UNSET)

        street_address_1 = d.pop("streetAddress1", UNSET)

        street_address_2 = d.pop("streetAddress2", UNSET)

        city = d.pop("city", UNSET)

        state_province = d.pop("stateProvince", UNSET)

        zip_postal_code = d.pop("zipPostalCode", UNSET)

        country = d.pop("country", UNSET)

        building = cls(
            name=name,
            id=id,
            street_address_1=street_address_1,
            street_address_2=street_address_2,
            city=city,
            state_province=state_province,
            zip_postal_code=zip_postal_code,
            country=country,
        )

        building.additional_properties = d
        return building

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
