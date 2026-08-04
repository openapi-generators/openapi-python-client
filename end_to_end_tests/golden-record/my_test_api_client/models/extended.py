from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from pydantic import ConfigDict, Field
from tandem_platform.schema.protected import BaseModel

from ..models.an_all_of_enum import AnAllOfEnum
from ..models.an_enum import AnEnum
from ..models.different_enum import DifferentEnum

if TYPE_CHECKING:
    from ..models.free_form_model import FreeFormModel
    from ..models.model_with_union_property import ModelWithUnionProperty


T = TypeVar("T", bound="Extended")


class Extended(BaseModel):
    """
    Attributes:
        an_enum_value (AnEnum): For testing Enums in all the ways they can be used
        an_allof_enum_with_overridden_default (AnAllOfEnum):  Default: AnAllOfEnum.OVERRIDDEN_DEFAULT.
        a_camel_date_time (datetime.date | datetime.datetime):
        a_date (datetime.date):
        a_nullable_date (datetime.date | None):
        a_uuid (UUID):
        a_nullable_uuid (None | UUID):  Default: UUID('07EF8B4D-AA09-4FFA-898D-C710796AFF41').
        required_nullable (None | str):
        required_not_nullable (str):
        one_of_models (Any | FreeFormModel | ModelWithUnionProperty):
        nullable_one_of_models (FreeFormModel | ModelWithUnionProperty | None):
        model (ModelWithUnionProperty):
        nullable_model (ModelWithUnionProperty | None):
        any_value (Any | Unset):  Default: 'default'.
        an_optional_allof_enum (AnAllOfEnum | Unset):
        nested_list_of_enums (list[list[DifferentEnum]] | Unset):
        a_not_required_date (datetime.date | Unset):
        a_not_required_uuid (UUID | Unset):
        attr_1_leading_digit (str | Unset):
        attr_leading_underscore (str | Unset):
        not_required_nullable (None | str | Unset):
        not_required_not_nullable (str | Unset):
        not_required_one_of_models (FreeFormModel | ModelWithUnionProperty | Unset):
        not_required_nullable_one_of_models (FreeFormModel | ModelWithUnionProperty | None | str | Unset):
        not_required_model (ModelWithUnionProperty | Unset):
        not_required_nullable_model (ModelWithUnionProperty | None | Unset):
        from_extended (str | Unset):
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    an_enum_value: AnEnum
    a_camel_date_time: datetime.date | datetime.datetime = Field(alias="aCamelDateTime")
    a_date: datetime.date
    a_nullable_date: datetime.date | None
    a_uuid: UUID
    required_nullable: None | str
    required_not_nullable: str
    one_of_models: Any | FreeFormModel | ModelWithUnionProperty
    nullable_one_of_models: FreeFormModel | ModelWithUnionProperty | None
    model: ModelWithUnionProperty
    nullable_model: ModelWithUnionProperty | None
    an_allof_enum_with_overridden_default: AnAllOfEnum = AnAllOfEnum.OVERRIDDEN_DEFAULT
    a_nullable_uuid: None | UUID = UUID("07EF8B4D-AA09-4FFA-898D-C710796AFF41")
    any_value: Any | None = "default"
    an_optional_allof_enum: AnAllOfEnum | None = None
    nested_list_of_enums: list[list[DifferentEnum]] | None = None
    a_not_required_date: datetime.date | None = None
    a_not_required_uuid: UUID | None = None
    attr_1_leading_digit: str | None = Field(default=None, alias="1_leading_digit")
    attr_leading_underscore: str | None = Field(default=None, alias="_leading_underscore")
    not_required_nullable: None | str = None
    not_required_not_nullable: str | None = None
    not_required_one_of_models: FreeFormModel | ModelWithUnionProperty | None = None
    not_required_nullable_one_of_models: FreeFormModel | ModelWithUnionProperty | None | str | None = None
    not_required_model: ModelWithUnionProperty | None = None
    not_required_nullable_model: ModelWithUnionProperty | None = None
    from_extended: str | None = Field(default=None, alias="fromExtended")

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)


from ..models.free_form_model import FreeFormModel
from ..models.model_with_union_property import ModelWithUnionProperty

Extended.model_rebuild()
