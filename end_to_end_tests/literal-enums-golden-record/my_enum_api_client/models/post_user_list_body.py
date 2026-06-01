from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from pydantic import ConfigDict
from tandem_platform.schema.protected import BaseModel

from .. import types
from ..models.an_all_of_enum import AnAllOfEnum
from ..models.an_enum import AnEnum
from ..models.an_enum_with_null import AnEnumWithNull
from ..models.different_enum import DifferentEnum

T = TypeVar("T", bound="PostUserListBody")


class PostUserListBody(BaseModel):
    """
    Attributes:
        an_enum_value (list[AnEnum] | Unset):
        an_enum_value_with_null (list[AnEnumWithNull | None] | Unset):
        an_enum_value_with_only_null (list[None] | Unset):
        an_allof_enum_with_overridden_default (AnAllOfEnum | Unset):  Default: 'overridden_default'.
        an_optional_allof_enum (AnAllOfEnum | Unset):
        nested_list_of_enums (list[list[DifferentEnum]] | Unset):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    an_enum_value: list[AnEnum] | None = None
    an_enum_value_with_null: list[AnEnumWithNull | None] | None = None
    an_enum_value_with_only_null: list[None] | None = None
    an_allof_enum_with_overridden_default: AnAllOfEnum | None = "overridden_default"
    an_optional_allof_enum: AnAllOfEnum | None = None
    nested_list_of_enums: list[list[DifferentEnum]] | None = None

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_unset=True, mode="json")

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        if "an_enum_value" in self.model_fields_set and self.an_enum_value is not None:
            for an_enum_value_item_element in self.an_enum_value:
                files.append(("an_enum_value", (None, str(an_enum_value_item_element).encode(), "text/plain")))

        if "an_enum_value_with_null" in self.model_fields_set and self.an_enum_value_with_null is not None:
            for an_enum_value_with_null_item_element in self.an_enum_value_with_null:
                if an_enum_value_with_null_item_element is None:
                    files.append(
                        (
                            "an_enum_value_with_null",
                            (None, str(an_enum_value_with_null_item_element).encode(), "text/plain"),
                        )
                    )
                else:
                    files.append(
                        (
                            "an_enum_value_with_null",
                            (None, str(an_enum_value_with_null_item_element).encode(), "text/plain"),
                        )
                    )

        if "an_enum_value_with_only_null" in self.model_fields_set and self.an_enum_value_with_only_null is not None:
            for an_enum_value_with_only_null_item_element in self.an_enum_value_with_only_null:
                files.append(
                    (
                        "an_enum_value_with_only_null",
                        (None, str(an_enum_value_with_only_null_item_element).encode(), "text/plain"),
                    )
                )

        if (
            "an_allof_enum_with_overridden_default" in self.model_fields_set
            and self.an_allof_enum_with_overridden_default is not None
        ):
            files.append(
                (
                    "an_allof_enum_with_overridden_default",
                    (None, str(self.an_allof_enum_with_overridden_default).encode(), "text/plain"),
                )
            )

        if "an_optional_allof_enum" in self.model_fields_set and self.an_optional_allof_enum is not None:
            files.append(("an_optional_allof_enum", (None, str(self.an_optional_allof_enum).encode(), "text/plain")))

        if "nested_list_of_enums" in self.model_fields_set and self.nested_list_of_enums is not None:
            for nested_list_of_enums_item_element in self.nested_list_of_enums:
                for nested_list_of_enums_item_item_element in nested_list_of_enums_item_element:
                    files.append(
                        (
                            "nested_list_of_enums",
                            (None, str(nested_list_of_enums_item_item_element).encode(), "text/plain"),
                        )
                    )

        for prop_name, prop in (self.__pydantic_extra__ or {}).items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files
