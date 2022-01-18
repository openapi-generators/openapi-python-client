import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.an_all_of_enum import AnAllOfEnum
from ..models.an_enum import AnEnum
from ..models.different_enum import DifferentEnum
from ..models.free_form_model import FreeFormModel
from ..models.model_with_union_property import ModelWithUnionProperty
from ..types import UNSET, Unset

T = TypeVar("T", bound="AModel")


@attr.s(auto_attribs=True)
class AModel:
    """A Model for testing all the ways custom objects can be used

    Attributes:
        an_enum_value (AnEnum): For testing Enums in all the ways they can be used
        an_allof_enum_with_overridden_default (AnAllOfEnum):  Default: AnAllOfEnum.OVERRIDDEN_DEFAULT.
        a_camel_date_time (Union[datetime.date, datetime.datetime]):
        a_date (datetime.date):
        required_not_nullable (str):
        one_of_models (Union[Any, FreeFormModel, ModelWithUnionProperty]):
        model (ModelWithUnionProperty):
        any_value (Union[Unset, Any]):
        an_optional_allof_enum (Union[Unset, AnAllOfEnum]):
        nested_list_of_enums (Union[Unset, List[List[DifferentEnum]]]):
        a_nullable_date (Optional[datetime.date]):
        a_not_required_date (Union[Unset, datetime.date]):
        attr_1_leading_digit (Union[Unset, str]):
        required_nullable (Optional[str]):
        not_required_nullable (Union[Unset, None, str]):
        not_required_not_nullable (Union[Unset, str]):
        nullable_one_of_models (Union[FreeFormModel, ModelWithUnionProperty, None]):
        not_required_one_of_models (Union[FreeFormModel, ModelWithUnionProperty, Unset]):
        not_required_nullable_one_of_models (Union[FreeFormModel, ModelWithUnionProperty, None, Unset, str]):
        nullable_model (Optional[ModelWithUnionProperty]):
        not_required_model (Union[Unset, ModelWithUnionProperty]):
        not_required_nullable_model (Union[Unset, None, ModelWithUnionProperty]):
    """

    an_enum_value: AnEnum
    a_camel_date_time: Union[datetime.date, datetime.datetime]
    a_date: datetime.date
    required_not_nullable: str
    one_of_models: Union[Any, FreeFormModel, ModelWithUnionProperty]
    model: ModelWithUnionProperty
    a_nullable_date: Optional[datetime.date]
    required_nullable: Optional[str]
    nullable_one_of_models: Union[FreeFormModel, ModelWithUnionProperty, None]
    nullable_model: Optional[ModelWithUnionProperty]
    an_allof_enum_with_overridden_default: AnAllOfEnum = AnAllOfEnum.OVERRIDDEN_DEFAULT
    any_value: Union[Unset, Any] = UNSET
    an_optional_allof_enum: Union[Unset, AnAllOfEnum] = UNSET
    nested_list_of_enums: Union[Unset, List[List[DifferentEnum]]] = UNSET
    a_not_required_date: Union[Unset, datetime.date] = UNSET
    attr_1_leading_digit: Union[Unset, str] = UNSET
    not_required_nullable: Union[Unset, None, str] = UNSET
    not_required_not_nullable: Union[Unset, str] = UNSET
    not_required_one_of_models: Union[FreeFormModel, ModelWithUnionProperty, Unset] = UNSET
    not_required_nullable_one_of_models: Union[FreeFormModel, ModelWithUnionProperty, None, Unset, str] = UNSET
    not_required_model: Union[Unset, ModelWithUnionProperty] = UNSET
    not_required_nullable_model: Union[Unset, None, ModelWithUnionProperty] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        an_enum_value = self.an_enum_value.value

        an_allof_enum_with_overridden_default = self.an_allof_enum_with_overridden_default.value

        if isinstance(self.a_camel_date_time, datetime.datetime):
            a_camel_date_time = self.a_camel_date_time.isoformat()

        else:
            a_camel_date_time = self.a_camel_date_time.isoformat()

        a_date = self.a_date.isoformat()
        required_not_nullable = self.required_not_nullable

        if isinstance(self.one_of_models, FreeFormModel):
            one_of_models = self.one_of_models.to_dict()

        elif isinstance(self.one_of_models, ModelWithUnionProperty):
            one_of_models = self.one_of_models.to_dict()

        else:
            one_of_models = self.one_of_models

        model = self.model.to_dict()

        any_value = self.any_value
        an_optional_allof_enum: Union[Unset, str] = UNSET
        if not isinstance(self.an_optional_allof_enum, Unset):
            an_optional_allof_enum = self.an_optional_allof_enum.value

        nested_list_of_enums: Union[Unset, List[List[str]]] = UNSET
        if not isinstance(self.nested_list_of_enums, Unset):
            nested_list_of_enums = []
            for nested_list_of_enums_item_data in self.nested_list_of_enums:
                nested_list_of_enums_item = []
                for nested_list_of_enums_item_item_data in nested_list_of_enums_item_data:
                    nested_list_of_enums_item_item = nested_list_of_enums_item_item_data.value

                    nested_list_of_enums_item.append(nested_list_of_enums_item_item)

                nested_list_of_enums.append(nested_list_of_enums_item)

        a_nullable_date = self.a_nullable_date.isoformat() if self.a_nullable_date else None
        a_not_required_date: Union[Unset, str] = UNSET
        if not isinstance(self.a_not_required_date, Unset):
            a_not_required_date = self.a_not_required_date.isoformat()

        attr_1_leading_digit = self.attr_1_leading_digit
        required_nullable = self.required_nullable
        not_required_nullable = self.not_required_nullable
        not_required_not_nullable = self.not_required_not_nullable
        nullable_one_of_models: Union[Dict[str, Any], None]
        if self.nullable_one_of_models is None:
            nullable_one_of_models = None

        elif isinstance(self.nullable_one_of_models, FreeFormModel):
            nullable_one_of_models = self.nullable_one_of_models.to_dict()

        else:
            nullable_one_of_models = self.nullable_one_of_models.to_dict()

        not_required_one_of_models: Union[Dict[str, Any], Unset]
        if isinstance(self.not_required_one_of_models, Unset):
            not_required_one_of_models = UNSET

        elif isinstance(self.not_required_one_of_models, FreeFormModel):
            not_required_one_of_models = UNSET
            if not isinstance(self.not_required_one_of_models, Unset):
                not_required_one_of_models = self.not_required_one_of_models.to_dict()

        else:
            not_required_one_of_models = UNSET
            if not isinstance(self.not_required_one_of_models, Unset):
                not_required_one_of_models = self.not_required_one_of_models.to_dict()

        not_required_nullable_one_of_models: Union[Dict[str, Any], None, Unset, str]
        if isinstance(self.not_required_nullable_one_of_models, Unset):
            not_required_nullable_one_of_models = UNSET
        elif self.not_required_nullable_one_of_models is None:
            not_required_nullable_one_of_models = None

        elif isinstance(self.not_required_nullable_one_of_models, FreeFormModel):
            not_required_nullable_one_of_models = UNSET
            if not isinstance(self.not_required_nullable_one_of_models, Unset):
                not_required_nullable_one_of_models = self.not_required_nullable_one_of_models.to_dict()

        elif isinstance(self.not_required_nullable_one_of_models, ModelWithUnionProperty):
            not_required_nullable_one_of_models = UNSET
            if not isinstance(self.not_required_nullable_one_of_models, Unset):
                not_required_nullable_one_of_models = self.not_required_nullable_one_of_models.to_dict()

        else:
            not_required_nullable_one_of_models = self.not_required_nullable_one_of_models

        nullable_model = self.nullable_model.to_dict() if self.nullable_model else None

        not_required_model: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.not_required_model, Unset):
            not_required_model = self.not_required_model.to_dict()

        not_required_nullable_model: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.not_required_nullable_model, Unset):
            not_required_nullable_model = (
                self.not_required_nullable_model.to_dict() if self.not_required_nullable_model else None
            )

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "an_enum_value": an_enum_value,
                "an_allof_enum_with_overridden_default": an_allof_enum_with_overridden_default,
                "aCamelDateTime": a_camel_date_time,
                "a_date": a_date,
                "required_not_nullable": required_not_nullable,
                "one_of_models": one_of_models,
                "model": model,
                "a_nullable_date": a_nullable_date,
                "required_nullable": required_nullable,
                "nullable_one_of_models": nullable_one_of_models,
                "nullable_model": nullable_model,
            }
        )
        if any_value is not UNSET:
            field_dict["any_value"] = any_value
        if an_optional_allof_enum is not UNSET:
            field_dict["an_optional_allof_enum"] = an_optional_allof_enum
        if nested_list_of_enums is not UNSET:
            field_dict["nested_list_of_enums"] = nested_list_of_enums
        if a_not_required_date is not UNSET:
            field_dict["a_not_required_date"] = a_not_required_date
        if attr_1_leading_digit is not UNSET:
            field_dict["1_leading_digit"] = attr_1_leading_digit
        if not_required_nullable is not UNSET:
            field_dict["not_required_nullable"] = not_required_nullable
        if not_required_not_nullable is not UNSET:
            field_dict["not_required_not_nullable"] = not_required_not_nullable
        if not_required_one_of_models is not UNSET:
            field_dict["not_required_one_of_models"] = not_required_one_of_models
        if not_required_nullable_one_of_models is not UNSET:
            field_dict["not_required_nullable_one_of_models"] = not_required_nullable_one_of_models
        if not_required_model is not UNSET:
            field_dict["not_required_model"] = not_required_model
        if not_required_nullable_model is not UNSET:
            field_dict["not_required_nullable_model"] = not_required_nullable_model

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        an_enum_value = AnEnum(d.pop("an_enum_value"))

        an_allof_enum_with_overridden_default = AnAllOfEnum(d.pop("an_allof_enum_with_overridden_default"))

        def _parse_a_camel_date_time(data: object) -> Union[datetime.date, datetime.datetime]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                a_camel_date_time_type_0 = isoparse(data)

                return a_camel_date_time_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, str):
                raise TypeError()
            a_camel_date_time_type_1 = isoparse(data).date()

            return a_camel_date_time_type_1

        a_camel_date_time = _parse_a_camel_date_time(d.pop("aCamelDateTime"))

        a_date = isoparse(d.pop("a_date")).date()

        required_not_nullable = d.pop("required_not_nullable")

        def _parse_one_of_models(data: object) -> Union[Any, FreeFormModel, ModelWithUnionProperty]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                one_of_models_type_0 = FreeFormModel.from_dict(data)

                return one_of_models_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                one_of_models_type_1 = ModelWithUnionProperty.from_dict(data)

                return one_of_models_type_1
            except:  # noqa: E722
                pass
            return cast(Union[Any, FreeFormModel, ModelWithUnionProperty], data)

        one_of_models = _parse_one_of_models(d.pop("one_of_models"))

        model = ModelWithUnionProperty.from_dict(d.pop("model"))

        any_value = d.pop("any_value", UNSET)

        _an_optional_allof_enum = d.pop("an_optional_allof_enum", UNSET)
        an_optional_allof_enum: Union[Unset, AnAllOfEnum]
        if isinstance(_an_optional_allof_enum, Unset):
            an_optional_allof_enum = UNSET
        else:
            an_optional_allof_enum = AnAllOfEnum(_an_optional_allof_enum)

        nested_list_of_enums = []
        _nested_list_of_enums = d.pop("nested_list_of_enums", UNSET)
        for nested_list_of_enums_item_data in _nested_list_of_enums or []:
            nested_list_of_enums_item = []
            _nested_list_of_enums_item = nested_list_of_enums_item_data
            for nested_list_of_enums_item_item_data in _nested_list_of_enums_item:
                nested_list_of_enums_item_item = DifferentEnum(nested_list_of_enums_item_item_data)

                nested_list_of_enums_item.append(nested_list_of_enums_item_item)

            nested_list_of_enums.append(nested_list_of_enums_item)

        _a_nullable_date = d.pop("a_nullable_date")
        a_nullable_date: Optional[datetime.date]
        if _a_nullable_date is None:
            a_nullable_date = None
        else:
            a_nullable_date = isoparse(_a_nullable_date).date()

        _a_not_required_date = d.pop("a_not_required_date", UNSET)
        a_not_required_date: Union[Unset, datetime.date]
        if isinstance(_a_not_required_date, Unset):
            a_not_required_date = UNSET
        else:
            a_not_required_date = isoparse(_a_not_required_date).date()

        attr_1_leading_digit = d.pop("1_leading_digit", UNSET)

        required_nullable = d.pop("required_nullable")

        not_required_nullable = d.pop("not_required_nullable", UNSET)

        not_required_not_nullable = d.pop("not_required_not_nullable", UNSET)

        def _parse_nullable_one_of_models(data: object) -> Union[FreeFormModel, ModelWithUnionProperty, None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                nullable_one_of_models_type_0 = FreeFormModel.from_dict(data)

                return nullable_one_of_models_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            nullable_one_of_models_type_1 = ModelWithUnionProperty.from_dict(data)

            return nullable_one_of_models_type_1

        nullable_one_of_models = _parse_nullable_one_of_models(d.pop("nullable_one_of_models"))

        def _parse_not_required_one_of_models(data: object) -> Union[FreeFormModel, ModelWithUnionProperty, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _not_required_one_of_models_type_0 = data
                not_required_one_of_models_type_0: Union[Unset, FreeFormModel]
                if isinstance(_not_required_one_of_models_type_0, Unset):
                    not_required_one_of_models_type_0 = UNSET
                else:
                    not_required_one_of_models_type_0 = FreeFormModel.from_dict(_not_required_one_of_models_type_0)

                return not_required_one_of_models_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            _not_required_one_of_models_type_1 = data
            not_required_one_of_models_type_1: Union[Unset, ModelWithUnionProperty]
            if isinstance(_not_required_one_of_models_type_1, Unset):
                not_required_one_of_models_type_1 = UNSET
            else:
                not_required_one_of_models_type_1 = ModelWithUnionProperty.from_dict(_not_required_one_of_models_type_1)

            return not_required_one_of_models_type_1

        not_required_one_of_models = _parse_not_required_one_of_models(d.pop("not_required_one_of_models", UNSET))

        def _parse_not_required_nullable_one_of_models(
            data: object,
        ) -> Union[FreeFormModel, ModelWithUnionProperty, None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _not_required_nullable_one_of_models_type_0 = data
                not_required_nullable_one_of_models_type_0: Union[Unset, FreeFormModel]
                if isinstance(_not_required_nullable_one_of_models_type_0, Unset):
                    not_required_nullable_one_of_models_type_0 = UNSET
                else:
                    not_required_nullable_one_of_models_type_0 = FreeFormModel.from_dict(
                        _not_required_nullable_one_of_models_type_0
                    )

                return not_required_nullable_one_of_models_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _not_required_nullable_one_of_models_type_1 = data
                not_required_nullable_one_of_models_type_1: Union[Unset, ModelWithUnionProperty]
                if isinstance(_not_required_nullable_one_of_models_type_1, Unset):
                    not_required_nullable_one_of_models_type_1 = UNSET
                else:
                    not_required_nullable_one_of_models_type_1 = ModelWithUnionProperty.from_dict(
                        _not_required_nullable_one_of_models_type_1
                    )

                return not_required_nullable_one_of_models_type_1
            except:  # noqa: E722
                pass
            return cast(Union[FreeFormModel, ModelWithUnionProperty, None, Unset, str], data)

        not_required_nullable_one_of_models = _parse_not_required_nullable_one_of_models(
            d.pop("not_required_nullable_one_of_models", UNSET)
        )

        _nullable_model = d.pop("nullable_model")
        nullable_model: Optional[ModelWithUnionProperty]
        if _nullable_model is None:
            nullable_model = None
        else:
            nullable_model = ModelWithUnionProperty.from_dict(_nullable_model)

        _not_required_model = d.pop("not_required_model", UNSET)
        not_required_model: Union[Unset, ModelWithUnionProperty]
        if isinstance(_not_required_model, Unset):
            not_required_model = UNSET
        else:
            not_required_model = ModelWithUnionProperty.from_dict(_not_required_model)

        _not_required_nullable_model = d.pop("not_required_nullable_model", UNSET)
        not_required_nullable_model: Union[Unset, None, ModelWithUnionProperty]
        if _not_required_nullable_model is None:
            not_required_nullable_model = None
        elif isinstance(_not_required_nullable_model, Unset):
            not_required_nullable_model = UNSET
        else:
            not_required_nullable_model = ModelWithUnionProperty.from_dict(_not_required_nullable_model)

        a_model = cls(
            an_enum_value=an_enum_value,
            an_allof_enum_with_overridden_default=an_allof_enum_with_overridden_default,
            a_camel_date_time=a_camel_date_time,
            a_date=a_date,
            required_not_nullable=required_not_nullable,
            one_of_models=one_of_models,
            model=model,
            any_value=any_value,
            an_optional_allof_enum=an_optional_allof_enum,
            nested_list_of_enums=nested_list_of_enums,
            a_nullable_date=a_nullable_date,
            a_not_required_date=a_not_required_date,
            attr_1_leading_digit=attr_1_leading_digit,
            required_nullable=required_nullable,
            not_required_nullable=not_required_nullable,
            not_required_not_nullable=not_required_not_nullable,
            nullable_one_of_models=nullable_one_of_models,
            not_required_one_of_models=not_required_one_of_models,
            not_required_nullable_one_of_models=not_required_nullable_one_of_models,
            nullable_model=nullable_model,
            not_required_model=not_required_model,
            not_required_nullable_model=not_required_nullable_model,
        )

        return a_model
