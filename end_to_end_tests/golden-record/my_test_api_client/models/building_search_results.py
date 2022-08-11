from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.building import Building
from ..types import UNSET, Unset

T = TypeVar("T", bound="BuildingSearchResults")


@attr.s(auto_attribs=True)
class BuildingSearchResults:
    """
    Attributes:
        total_count (Union[Unset, int]):  Example: 3.
        results (Union[Unset, List[Building]]):
    """

    total_count: Union[Unset, int] = UNSET
    results: Union[Unset, List[Building]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        total_count = self.total_count
        results: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.results, Unset):
            results = []
            for results_item_data in self.results:
                results_item = results_item_data.to_dict()

                results.append(results_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if total_count is not UNSET:
            field_dict["totalCount"] = total_count
        if results is not UNSET:
            field_dict["results"] = results

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        total_count = d.pop("totalCount", UNSET)

        results = []
        _results = d.pop("results", UNSET)
        for results_item_data in _results or []:
            results_item = Building.from_dict(results_item_data)

            results.append(results_item)

        building_search_results = cls(
            total_count=total_count,
            results=results,
        )

        building_search_results.additional_properties = d
        return building_search_results

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
