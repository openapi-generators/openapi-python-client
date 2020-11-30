from typing import Any, Dict, List

import attr


@attr.s(auto_attribs=True)
class FreeFormModel:
    """  """

    _additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        field_dict.update(self._additional_properties)
        field_dict.update({})

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "FreeFormModel":
        d = src_dict.copy()
        free_form_model = FreeFormModel()

        free_form_model._additional_properties = d
        return free_form_model

    @property
    def additional_properties(self) -> Dict[str, Any]:
        return self._additional_properties

    @property
    def additional_keys(self) -> List[str]:
        return list(self._additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self._additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self._additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self._additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self._additional_properties
