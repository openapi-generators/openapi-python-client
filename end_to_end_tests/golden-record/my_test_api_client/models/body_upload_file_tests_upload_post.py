from typing import Any, Dict, Optional, Set

import attr

from ..types import UNSET, File


@attr.s(auto_attribs=True)
class BodyUploadFileTestsUploadPost:
    """  """

    some_file: File

    def to_dict(
        self,
        include: Optional[Set[str]] = None,
        exclude: Optional[Set[str]] = None,
        exclude_unset: bool = False,
        exclude_none: bool = False,
    ) -> Dict[str, Any]:
        some_file = self.some_file.to_tuple()

        all_properties = {
            "some_file": some_file,
        }

        trimmed_properties: Dict[str, Any] = {}
        for property_name, property_value in all_properties.items():
            if include is not None and property_name not in include:
                continue
            if exclude is not None and property_name in exclude:
                continue
            if exclude_unset and property_value is UNSET:
                continue
            if exclude_none and property_value is None:
                continue
            trimmed_properties[property_name] = property_value

        return trimmed_properties

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "BodyUploadFileTestsUploadPost":
        some_file = d["some_file"]

        return BodyUploadFileTestsUploadPost(
            some_file=some_file,
        )
