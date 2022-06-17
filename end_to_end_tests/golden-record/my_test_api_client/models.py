""" Contains all the data models used in inputs/outputs """

from __future__ import annotations

import datetime
import json
from enum import Enum, IntEnum
from io import BytesIO
from typing import Any, Dict, List, Optional, Tuple, Type, Union, cast

import attr
from dateutil.parser import isoparse

from .types import UNSET, File, FileJsonType, Unset


class AnEnum(str, Enum):
    FIRST_VALUE = "FIRST_VALUE"
    SECOND_VALUE = "SECOND_VALUE"

    def __str__(self) -> str:
        return str(self.value)


class AnEnumWithNull(str, Enum):
    FIRST_VALUE = "FIRST_VALUE"
    SECOND_VALUE = "SECOND_VALUE"

    def __str__(self) -> str:
        return str(self.value)


class AnAllOfEnum(str, Enum):
    FOO = "foo"
    BAR = "bar"
    A_DEFAULT = "a_default"
    OVERRIDDEN_DEFAULT = "overridden_default"

    def __str__(self) -> str:
        return str(self.value)


class AnIntEnum(IntEnum):
    VALUE_NEGATIVE_1 = -1
    VALUE_1 = 1
    VALUE_2 = 2

    def __str__(self) -> str:
        return str(self.value)


class DifferentEnum(str, Enum):
    DIFFERENT = "DIFFERENT"
    OTHER = "OTHER"

    def __str__(self) -> str:
        return str(self.value)


class AllOfSubModelTypeEnum(IntEnum):
    VALUE_0 = 0
    VALUE_1 = 1

    def __str__(self) -> str:
        return str(self.value)


class AnotherAllOfSubModelType(str, Enum):
    SUBMODEL = "submodel"

    def __str__(self) -> str:
        return str(self.value)


class AnotherAllOfSubModelTypeEnum(IntEnum):
    VALUE_0 = 0

    def __str__(self) -> str:
        return str(self.value)


@attr.s(auto_attribs=True)
class AFormData:
    """
    Attributes:
        an_required_field (str):
        an_optional_field (Union[Unset, str]):
    """

    an_required_field: str
    an_optional_field: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        an_required_field = self.an_required_field
        an_optional_field = self.an_optional_field

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "an_required_field": an_required_field,
            }
        )
        if an_optional_field is not UNSET:
            field_dict["an_optional_field"] = an_optional_field

        return field_dict

    @classmethod
    def from_dict(cls: Type[AFormData], src_dict: Dict[str, Any]) -> AFormData:
        d = src_dict.copy()
        an_required_field = d.pop("an_required_field")

        an_optional_field = d.pop("an_optional_field", UNSET)

        a_form_data = cls(
            an_required_field=an_required_field,
            an_optional_field=an_optional_field,
        )

        a_form_data.additional_properties = d
        return a_form_data

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


@attr.s(auto_attribs=True)
class ValidationError:
    """
    Attributes:
        loc (List[str]):
        msg (str):
        type (str):
    """

    loc: List[str]
    msg: str
    type: str

    def to_dict(self) -> Dict[str, Any]:
        loc = self.loc

        msg = self.msg
        type = self.type

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "loc": loc,
                "msg": msg,
                "type": type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[ValidationError], src_dict: Dict[str, Any]) -> ValidationError:
        d = src_dict.copy()
        loc = cast(List[str], d.pop("loc"))

        msg = d.pop("msg")

        type = d.pop("type")

        validation_error = cls(
            loc=loc,
            msg=msg,
            type=type,
        )

        return validation_error


@attr.s(auto_attribs=True)
class ModelWithUnionProperty:
    """
    Attributes:
        a_property (Union[AnEnum, AnIntEnum, Unset]):
    """

    a_property: Union[AnEnum, AnIntEnum, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        a_property: Union[Unset, int, str]
        if isinstance(self.a_property, Unset):
            a_property = UNSET

        elif isinstance(self.a_property, AnEnum):
            a_property = UNSET
            if not isinstance(self.a_property, Unset):
                a_property = self.a_property.value

        else:
            a_property = UNSET
            if not isinstance(self.a_property, Unset):
                a_property = self.a_property.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if a_property is not UNSET:
            field_dict["a_property"] = a_property

        return field_dict

    @classmethod
    def from_dict(cls: Type[ModelWithUnionProperty], src_dict: Dict[str, Any]) -> ModelWithUnionProperty:
        d = src_dict.copy()

        def _parse_a_property(data: object) -> Union[AnEnum, AnIntEnum, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                _a_property_type_0 = data
                a_property_type_0: Union[Unset, AnEnum]
                if isinstance(_a_property_type_0, Unset):
                    a_property_type_0 = UNSET
                else:
                    a_property_type_0 = AnEnum(_a_property_type_0)

                return a_property_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, int):
                raise TypeError()
            _a_property_type_1 = data
            a_property_type_1: Union[Unset, AnIntEnum]
            if isinstance(_a_property_type_1, Unset):
                a_property_type_1 = UNSET
            else:
                a_property_type_1 = AnIntEnum(_a_property_type_1)

            return a_property_type_1

        a_property = _parse_a_property(d.pop("a_property", UNSET))

        model_with_union_property = cls(
            a_property=a_property,
        )

        return model_with_union_property


@attr.s(auto_attribs=True)
class ModelWithUnionPropertyInlinedFruitType0:
    """
    Attributes:
        apples (Union[Unset, str]):
    """

    apples: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        apples = self.apples

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if apples is not UNSET:
            field_dict["apples"] = apples

        return field_dict

    @classmethod
    def from_dict(
        cls: Type[ModelWithUnionPropertyInlinedFruitType0], src_dict: Dict[str, Any]
    ) -> ModelWithUnionPropertyInlinedFruitType0:
        d = src_dict.copy()
        apples = d.pop("apples", UNSET)

        model_with_union_property_inlined_fruit_type_0 = cls(
            apples=apples,
        )

        model_with_union_property_inlined_fruit_type_0.additional_properties = d
        return model_with_union_property_inlined_fruit_type_0

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


@attr.s(auto_attribs=True)
class ModelWithUnionPropertyInlinedFruitType1:
    """
    Attributes:
        bananas (Union[Unset, str]):
    """

    bananas: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        bananas = self.bananas

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if bananas is not UNSET:
            field_dict["bananas"] = bananas

        return field_dict

    @classmethod
    def from_dict(
        cls: Type[ModelWithUnionPropertyInlinedFruitType1], src_dict: Dict[str, Any]
    ) -> ModelWithUnionPropertyInlinedFruitType1:
        d = src_dict.copy()
        bananas = d.pop("bananas", UNSET)

        model_with_union_property_inlined_fruit_type_1 = cls(
            bananas=bananas,
        )

        model_with_union_property_inlined_fruit_type_1.additional_properties = d
        return model_with_union_property_inlined_fruit_type_1

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


@attr.s(auto_attribs=True)
class ModelWithUnionPropertyInlined:
    """
    Attributes:
        fruit (Union[ModelWithUnionPropertyInlinedFruitType0, ModelWithUnionPropertyInlinedFruitType1, Unset]):
    """

    fruit: Union[ModelWithUnionPropertyInlinedFruitType0, ModelWithUnionPropertyInlinedFruitType1, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        fruit: Union[Dict[str, Any], Unset]
        if isinstance(self.fruit, Unset):
            fruit = UNSET

        elif isinstance(self.fruit, ModelWithUnionPropertyInlinedFruitType0):
            fruit = UNSET
            if not isinstance(self.fruit, Unset):
                fruit = self.fruit.to_dict()

        else:
            fruit = UNSET
            if not isinstance(self.fruit, Unset):
                fruit = self.fruit.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if fruit is not UNSET:
            field_dict["fruit"] = fruit

        return field_dict

    @classmethod
    def from_dict(cls: Type[ModelWithUnionPropertyInlined], src_dict: Dict[str, Any]) -> ModelWithUnionPropertyInlined:
        d = src_dict.copy()

        def _parse_fruit(
            data: object,
        ) -> Union[ModelWithUnionPropertyInlinedFruitType0, ModelWithUnionPropertyInlinedFruitType1, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _fruit_type_0 = data
                fruit_type_0: Union[Unset, ModelWithUnionPropertyInlinedFruitType0]
                if isinstance(_fruit_type_0, Unset):
                    fruit_type_0 = UNSET
                else:
                    fruit_type_0 = ModelWithUnionPropertyInlinedFruitType0.from_dict(_fruit_type_0)

                return fruit_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            _fruit_type_1 = data
            fruit_type_1: Union[Unset, ModelWithUnionPropertyInlinedFruitType1]
            if isinstance(_fruit_type_1, Unset):
                fruit_type_1 = UNSET
            else:
                fruit_type_1 = ModelWithUnionPropertyInlinedFruitType1.from_dict(_fruit_type_1)

            return fruit_type_1

        fruit = _parse_fruit(d.pop("fruit", UNSET))

        model_with_union_property_inlined = cls(
            fruit=fruit,
        )

        return model_with_union_property_inlined


@attr.s(auto_attribs=True)
class FreeFormModel:
    """ """

    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[FreeFormModel], src_dict: Dict[str, Any]) -> FreeFormModel:
        d = src_dict.copy()
        free_form_model = cls()

        free_form_model.additional_properties = d
        return free_form_model

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


@attr.s(auto_attribs=True)
class ModelWithAdditionalPropertiesInlinedAdditionalProperty:
    """
    Attributes:
        extra_props_prop (Union[Unset, str]):
    """

    extra_props_prop: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        extra_props_prop = self.extra_props_prop

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if extra_props_prop is not UNSET:
            field_dict["extra_props_prop"] = extra_props_prop

        return field_dict

    @classmethod
    def from_dict(
        cls: Type[ModelWithAdditionalPropertiesInlinedAdditionalProperty], src_dict: Dict[str, Any]
    ) -> ModelWithAdditionalPropertiesInlinedAdditionalProperty:
        d = src_dict.copy()
        extra_props_prop = d.pop("extra_props_prop", UNSET)

        model_with_additional_properties_inlined_additional_property = cls(
            extra_props_prop=extra_props_prop,
        )

        model_with_additional_properties_inlined_additional_property.additional_properties = d
        return model_with_additional_properties_inlined_additional_property

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


@attr.s(auto_attribs=True)
class ModelWithAdditionalPropertiesInlined:
    """
    Attributes:
        a_number (Union[Unset, float]):
    """

    a_number: Union[Unset, float] = UNSET
    additional_properties: Dict[str, ModelWithAdditionalPropertiesInlinedAdditionalProperty] = attr.ib(
        init=False, factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:
        a_number = self.a_number

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})
        if a_number is not UNSET:
            field_dict["a_number"] = a_number

        return field_dict

    @classmethod
    def from_dict(
        cls: Type[ModelWithAdditionalPropertiesInlined], src_dict: Dict[str, Any]
    ) -> ModelWithAdditionalPropertiesInlined:
        d = src_dict.copy()
        a_number = d.pop("a_number", UNSET)

        model_with_additional_properties_inlined = cls(
            a_number=a_number,
        )

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = ModelWithAdditionalPropertiesInlinedAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        model_with_additional_properties_inlined.additional_properties = additional_properties
        return model_with_additional_properties_inlined

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> ModelWithAdditionalPropertiesInlinedAdditionalProperty:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: ModelWithAdditionalPropertiesInlinedAdditionalProperty) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties


@attr.s(auto_attribs=True)
class ModelWithPrimitiveAdditionalPropertiesADateHolder:
    """ """

    additional_properties: Dict[str, datetime.datetime] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.isoformat()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(
        cls: Type[ModelWithPrimitiveAdditionalPropertiesADateHolder], src_dict: Dict[str, Any]
    ) -> ModelWithPrimitiveAdditionalPropertiesADateHolder:
        d = src_dict.copy()
        model_with_primitive_additional_properties_a_date_holder = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = isoparse(prop_dict)

            additional_properties[prop_name] = additional_property

        model_with_primitive_additional_properties_a_date_holder.additional_properties = additional_properties
        return model_with_primitive_additional_properties_a_date_holder

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> datetime.datetime:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: datetime.datetime) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties


@attr.s(auto_attribs=True)
class ModelWithPrimitiveAdditionalProperties:
    """
    Attributes:
        a_date_holder (Union[Unset, ModelWithPrimitiveAdditionalPropertiesADateHolder]):
    """

    a_date_holder: Union[Unset, ModelWithPrimitiveAdditionalPropertiesADateHolder] = UNSET
    additional_properties: Dict[str, str] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        a_date_holder: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.a_date_holder, Unset):
            a_date_holder = self.a_date_holder.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if a_date_holder is not UNSET:
            field_dict["a_date_holder"] = a_date_holder

        return field_dict

    @classmethod
    def from_dict(
        cls: Type[ModelWithPrimitiveAdditionalProperties], src_dict: Dict[str, Any]
    ) -> ModelWithPrimitiveAdditionalProperties:
        d = src_dict.copy()
        _a_date_holder = d.pop("a_date_holder", UNSET)
        a_date_holder: Union[Unset, ModelWithPrimitiveAdditionalPropertiesADateHolder]
        if isinstance(_a_date_holder, Unset):
            a_date_holder = UNSET
        else:
            a_date_holder = ModelWithPrimitiveAdditionalPropertiesADateHolder.from_dict(_a_date_holder)

        model_with_primitive_additional_properties = cls(
            a_date_holder=a_date_holder,
        )

        model_with_primitive_additional_properties.additional_properties = d
        return model_with_primitive_additional_properties

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> str:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: str) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties


@attr.s(auto_attribs=True)
class ModelWithAdditionalPropertiesRefed:
    """ """

    additional_properties: Dict[str, AnEnum] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.value

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(
        cls: Type[ModelWithAdditionalPropertiesRefed], src_dict: Dict[str, Any]
    ) -> ModelWithAdditionalPropertiesRefed:
        d = src_dict.copy()
        model_with_additional_properties_refed = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = AnEnum(prop_dict)

            additional_properties[prop_name] = additional_property

        model_with_additional_properties_refed.additional_properties = additional_properties
        return model_with_additional_properties_refed

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> AnEnum:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: AnEnum) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties


@attr.s(auto_attribs=True)
class ModelWithAnyJsonPropertiesAdditionalPropertyType0:
    """ """

    additional_properties: Dict[str, str] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(
        cls: Type[ModelWithAnyJsonPropertiesAdditionalPropertyType0], src_dict: Dict[str, Any]
    ) -> ModelWithAnyJsonPropertiesAdditionalPropertyType0:
        d = src_dict.copy()
        model_with_any_json_properties_additional_property_type_0 = cls()

        model_with_any_json_properties_additional_property_type_0.additional_properties = d
        return model_with_any_json_properties_additional_property_type_0

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> str:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: str) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties


@attr.s(auto_attribs=True)
class ModelWithAnyJsonProperties:
    """ """

    additional_properties: Dict[
        str, Union[List[str], ModelWithAnyJsonPropertiesAdditionalPropertyType0, bool, float, int, str]
    ] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():

            if isinstance(prop, ModelWithAnyJsonPropertiesAdditionalPropertyType0):
                field_dict[prop_name] = prop.to_dict()

            elif isinstance(prop, list):
                field_dict[prop_name] = prop

            else:
                field_dict[prop_name] = prop

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[ModelWithAnyJsonProperties], src_dict: Dict[str, Any]) -> ModelWithAnyJsonProperties:
        d = src_dict.copy()
        model_with_any_json_properties = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(
                data: object,
            ) -> Union[List[str], ModelWithAnyJsonPropertiesAdditionalPropertyType0, bool, float, int, str]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_0 = ModelWithAnyJsonPropertiesAdditionalPropertyType0.from_dict(data)

                    return additional_property_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, list):
                        raise TypeError()
                    additional_property_type_1 = cast(List[str], data)

                    return additional_property_type_1
                except:  # noqa: E722
                    pass
                return cast(
                    Union[List[str], ModelWithAnyJsonPropertiesAdditionalPropertyType0, bool, float, int, str], data
                )

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        model_with_any_json_properties.additional_properties = additional_properties
        return model_with_any_json_properties

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(
        self, key: str
    ) -> Union[List[str], ModelWithAnyJsonPropertiesAdditionalPropertyType0, bool, float, int, str]:
        return self.additional_properties[key]

    def __setitem__(
        self,
        key: str,
        value: Union[List[str], ModelWithAnyJsonPropertiesAdditionalPropertyType0, bool, float, int, str],
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties


@attr.s(auto_attribs=True)
class AllOfSubModel:
    """
    Attributes:
        a_sub_property (Union[Unset, str]):
        type (Union[Unset, str]):
        type_enum (Union[Unset, AllOfSubModelTypeEnum]):
    """

    a_sub_property: Union[Unset, str] = UNSET
    type: Union[Unset, str] = UNSET
    type_enum: Union[Unset, AllOfSubModelTypeEnum] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        a_sub_property = self.a_sub_property
        type = self.type
        type_enum: Union[Unset, int] = UNSET
        if not isinstance(self.type_enum, Unset):
            type_enum = self.type_enum.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if a_sub_property is not UNSET:
            field_dict["a_sub_property"] = a_sub_property
        if type is not UNSET:
            field_dict["type"] = type
        if type_enum is not UNSET:
            field_dict["type_enum"] = type_enum

        return field_dict

    @classmethod
    def from_dict(cls: Type[AllOfSubModel], src_dict: Dict[str, Any]) -> AllOfSubModel:
        d = src_dict.copy()
        a_sub_property = d.pop("a_sub_property", UNSET)

        type = d.pop("type", UNSET)

        _type_enum = d.pop("type_enum", UNSET)
        type_enum: Union[Unset, AllOfSubModelTypeEnum]
        if isinstance(_type_enum, Unset):
            type_enum = UNSET
        else:
            type_enum = AllOfSubModelTypeEnum(_type_enum)

        all_of_sub_model = cls(
            a_sub_property=a_sub_property,
            type=type,
            type_enum=type_enum,
        )

        all_of_sub_model.additional_properties = d
        return all_of_sub_model

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


@attr.s(auto_attribs=True)
class AnotherAllOfSubModel:
    """
    Attributes:
        another_sub_property (Union[Unset, str]):
        type (Union[Unset, AnotherAllOfSubModelType]):
        type_enum (Union[Unset, AnotherAllOfSubModelTypeEnum]):
    """

    another_sub_property: Union[Unset, str] = UNSET
    type: Union[Unset, AnotherAllOfSubModelType] = UNSET
    type_enum: Union[Unset, AnotherAllOfSubModelTypeEnum] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        another_sub_property = self.another_sub_property
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        type_enum: Union[Unset, int] = UNSET
        if not isinstance(self.type_enum, Unset):
            type_enum = self.type_enum.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if another_sub_property is not UNSET:
            field_dict["another_sub_property"] = another_sub_property
        if type is not UNSET:
            field_dict["type"] = type
        if type_enum is not UNSET:
            field_dict["type_enum"] = type_enum

        return field_dict

    @classmethod
    def from_dict(cls: Type[AnotherAllOfSubModel], src_dict: Dict[str, Any]) -> AnotherAllOfSubModel:
        d = src_dict.copy()
        another_sub_property = d.pop("another_sub_property", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, AnotherAllOfSubModelType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = AnotherAllOfSubModelType(_type)

        _type_enum = d.pop("type_enum", UNSET)
        type_enum: Union[Unset, AnotherAllOfSubModelTypeEnum]
        if isinstance(_type_enum, Unset):
            type_enum = UNSET
        else:
            type_enum = AnotherAllOfSubModelTypeEnum(_type_enum)

        another_all_of_sub_model = cls(
            another_sub_property=another_sub_property,
            type=type,
            type_enum=type_enum,
        )

        another_all_of_sub_model.additional_properties = d
        return another_all_of_sub_model

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


@attr.s(auto_attribs=True)
class ModelName:
    """ """

    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[ModelName], src_dict: Dict[str, Any]) -> ModelName:
        d = src_dict.copy()
        model_name = cls()

        model_name.additional_properties = d
        return model_name

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


@attr.s(auto_attribs=True)
class ModelWithPropertyRef:
    """
    Attributes:
        inner (Union[Unset, ModelName]):
    """

    inner: Union[Unset, ModelName] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        inner: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.inner, Unset):
            inner = self.inner.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if inner is not UNSET:
            field_dict["inner"] = inner

        return field_dict

    @classmethod
    def from_dict(cls: Type[ModelWithPropertyRef], src_dict: Dict[str, Any]) -> ModelWithPropertyRef:
        d = src_dict.copy()
        _inner = d.pop("inner", UNSET)
        inner: Union[Unset, ModelName]
        if isinstance(_inner, Unset):
            inner = UNSET
        else:
            inner = ModelName.from_dict(_inner)

        model_with_property_ref = cls(
            inner=inner,
        )

        model_with_property_ref.additional_properties = d
        return model_with_property_ref

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


@attr.s(auto_attribs=True)
class ModelWithDateTimeProperty:
    """
    Attributes:
        datetime_ (Union[Unset, datetime.datetime]):
    """

    datetime_: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        datetime_: Union[Unset, str] = UNSET
        if not isinstance(self.datetime_, Unset):
            datetime_ = self.datetime_.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if datetime_ is not UNSET:
            field_dict["datetime"] = datetime_

        return field_dict

    @classmethod
    def from_dict(cls: Type[ModelWithDateTimeProperty], src_dict: Dict[str, Any]) -> ModelWithDateTimeProperty:
        d = src_dict.copy()
        _datetime_ = d.pop("datetime", UNSET)
        datetime_: Union[Unset, datetime.datetime]
        if isinstance(_datetime_, Unset):
            datetime_ = UNSET
        else:
            datetime_ = isoparse(_datetime_)

        model_with_date_time_property = cls(
            datetime_=datetime_,
        )

        model_with_date_time_property.additional_properties = d
        return model_with_date_time_property

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


@attr.s(auto_attribs=True)
class Import:
    """ """

    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[Import], src_dict: Dict[str, Any]) -> Import:
        d = src_dict.copy()
        import_ = cls()

        import_.additional_properties = d
        return import_

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


@attr.s(auto_attribs=True)
class None_:
    """ """

    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[None_], src_dict: Dict[str, Any]) -> None_:
        d = src_dict.copy()
        none = cls()

        none.additional_properties = d
        return none

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


@attr.s(auto_attribs=True)
class ModelReferenceWithPeriods:
    """A Model with periods in its reference"""

    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[ModelReferenceWithPeriods], src_dict: Dict[str, Any]) -> ModelReferenceWithPeriods:
        d = src_dict.copy()
        model_reference_with_periods = cls()

        model_reference_with_periods.additional_properties = d
        return model_reference_with_periods

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
    def from_dict(cls: Type[AModel], src_dict: Dict[str, Any]) -> AModel:
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


@attr.s(auto_attribs=True)
class BodyUploadFileTestsUploadPostSomeObject:
    """
    Attributes:
        num (float):
        text (str):
    """

    num: float
    text: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        num = self.num
        text = self.text

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "num": num,
                "text": text,
            }
        )

        return field_dict

    @classmethod
    def from_dict(
        cls: Type[BodyUploadFileTestsUploadPostSomeObject], src_dict: Dict[str, Any]
    ) -> BodyUploadFileTestsUploadPostSomeObject:
        d = src_dict.copy()
        num = d.pop("num")

        text = d.pop("text")

        body_upload_file_tests_upload_post_some_object = cls(
            num=num,
            text=text,
        )

        body_upload_file_tests_upload_post_some_object.additional_properties = d
        return body_upload_file_tests_upload_post_some_object

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


@attr.s(auto_attribs=True)
class BodyUploadFileTestsUploadPostSomeOptionalObject:
    """
    Attributes:
        foo (str):
    """

    foo: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        foo = self.foo

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "foo": foo,
            }
        )

        return field_dict

    @classmethod
    def from_dict(
        cls: Type[BodyUploadFileTestsUploadPostSomeOptionalObject], src_dict: Dict[str, Any]
    ) -> BodyUploadFileTestsUploadPostSomeOptionalObject:
        d = src_dict.copy()
        foo = d.pop("foo")

        body_upload_file_tests_upload_post_some_optional_object = cls(
            foo=foo,
        )

        body_upload_file_tests_upload_post_some_optional_object.additional_properties = d
        return body_upload_file_tests_upload_post_some_optional_object

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


@attr.s(auto_attribs=True)
class BodyUploadFileTestsUploadPostSomeNullableObject:
    """
    Attributes:
        bar (Union[Unset, str]):
    """

    bar: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        bar = self.bar

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if bar is not UNSET:
            field_dict["bar"] = bar

        return field_dict

    @classmethod
    def from_dict(
        cls: Type[BodyUploadFileTestsUploadPostSomeNullableObject], src_dict: Dict[str, Any]
    ) -> BodyUploadFileTestsUploadPostSomeNullableObject:
        d = src_dict.copy()
        bar = d.pop("bar", UNSET)

        body_upload_file_tests_upload_post_some_nullable_object = cls(
            bar=bar,
        )

        body_upload_file_tests_upload_post_some_nullable_object.additional_properties = d
        return body_upload_file_tests_upload_post_some_nullable_object

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


@attr.s(auto_attribs=True)
class BodyUploadFileTestsUploadPostAdditionalProperty:
    """
    Attributes:
        foo (Union[Unset, str]):
    """

    foo: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        foo = self.foo

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if foo is not UNSET:
            field_dict["foo"] = foo

        return field_dict

    @classmethod
    def from_dict(
        cls: Type[BodyUploadFileTestsUploadPostAdditionalProperty], src_dict: Dict[str, Any]
    ) -> BodyUploadFileTestsUploadPostAdditionalProperty:
        d = src_dict.copy()
        foo = d.pop("foo", UNSET)

        body_upload_file_tests_upload_post_additional_property = cls(
            foo=foo,
        )

        body_upload_file_tests_upload_post_additional_property.additional_properties = d
        return body_upload_file_tests_upload_post_additional_property

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


@attr.s(auto_attribs=True)
class BodyUploadFileTestsUploadPost:
    """
    Attributes:
        some_file (File):
        some_object (BodyUploadFileTestsUploadPostSomeObject):
        some_optional_file (Union[Unset, File]):
        some_string (Union[Unset, str]):  Default: 'some_default_string'.
        a_datetime (Union[Unset, datetime.datetime]):
        a_date (Union[Unset, datetime.date]):
        some_number (Union[Unset, float]):
        some_array (Union[Unset, List[float]]):
        some_optional_object (Union[Unset, BodyUploadFileTestsUploadPostSomeOptionalObject]):
        some_nullable_object (Optional[BodyUploadFileTestsUploadPostSomeNullableObject]):
        some_enum (Union[Unset, DifferentEnum]): An enumeration.
    """

    some_file: File
    some_object: BodyUploadFileTestsUploadPostSomeObject
    some_nullable_object: Optional[BodyUploadFileTestsUploadPostSomeNullableObject]
    some_optional_file: Union[Unset, File] = UNSET
    some_string: Union[Unset, str] = "some_default_string"
    a_datetime: Union[Unset, datetime.datetime] = UNSET
    a_date: Union[Unset, datetime.date] = UNSET
    some_number: Union[Unset, float] = UNSET
    some_array: Union[Unset, List[float]] = UNSET
    some_optional_object: Union[Unset, BodyUploadFileTestsUploadPostSomeOptionalObject] = UNSET
    some_enum: Union[Unset, DifferentEnum] = UNSET
    additional_properties: Dict[str, BodyUploadFileTestsUploadPostAdditionalProperty] = attr.ib(
        init=False, factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:
        some_file = self.some_file.to_tuple()

        some_object = self.some_object.to_dict()

        some_optional_file: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.some_optional_file, Unset):
            some_optional_file = self.some_optional_file.to_tuple()

        some_string = self.some_string
        a_datetime: Union[Unset, str] = UNSET
        if not isinstance(self.a_datetime, Unset):
            a_datetime = self.a_datetime.isoformat()

        a_date: Union[Unset, str] = UNSET
        if not isinstance(self.a_date, Unset):
            a_date = self.a_date.isoformat()

        some_number = self.some_number
        some_array: Union[Unset, List[float]] = UNSET
        if not isinstance(self.some_array, Unset):
            some_array = self.some_array

        some_optional_object: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.some_optional_object, Unset):
            some_optional_object = self.some_optional_object.to_dict()

        some_nullable_object = self.some_nullable_object.to_dict() if self.some_nullable_object else None

        some_enum: Union[Unset, str] = UNSET
        if not isinstance(self.some_enum, Unset):
            some_enum = self.some_enum.value

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update(
            {
                "some_file": some_file,
                "some_object": some_object,
                "some_nullable_object": some_nullable_object,
            }
        )
        if some_optional_file is not UNSET:
            field_dict["some_optional_file"] = some_optional_file
        if some_string is not UNSET:
            field_dict["some_string"] = some_string
        if a_datetime is not UNSET:
            field_dict["a_datetime"] = a_datetime
        if a_date is not UNSET:
            field_dict["a_date"] = a_date
        if some_number is not UNSET:
            field_dict["some_number"] = some_number
        if some_array is not UNSET:
            field_dict["some_array"] = some_array
        if some_optional_object is not UNSET:
            field_dict["some_optional_object"] = some_optional_object
        if some_enum is not UNSET:
            field_dict["some_enum"] = some_enum

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        some_file = self.some_file.to_tuple()

        some_object = (None, json.dumps(self.some_object.to_dict()).encode(), "application/json")

        some_optional_file: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.some_optional_file, Unset):
            some_optional_file = self.some_optional_file.to_tuple()

        some_string = (
            self.some_string
            if isinstance(self.some_string, Unset)
            else (None, str(self.some_string).encode(), "text/plain")
        )
        a_datetime: Union[Unset, bytes] = UNSET
        if not isinstance(self.a_datetime, Unset):
            a_datetime = self.a_datetime.isoformat().encode()

        a_date: Union[Unset, bytes] = UNSET
        if not isinstance(self.a_date, Unset):
            a_date = self.a_date.isoformat().encode()

        some_number = (
            self.some_number
            if isinstance(self.some_number, Unset)
            else (None, str(self.some_number).encode(), "text/plain")
        )
        some_array: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.some_array, Unset):
            _temp_some_array = self.some_array
            some_array = (None, json.dumps(_temp_some_array).encode(), "application/json")

        some_optional_object: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.some_optional_object, Unset):
            some_optional_object = (None, json.dumps(self.some_optional_object.to_dict()).encode(), "application/json")

        some_nullable_object = (
            (None, json.dumps(self.some_nullable_object.to_dict()).encode(), "application/json")
            if self.some_nullable_object
            else None
        )

        some_enum: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.some_enum, Unset):
            some_enum = (None, str(self.some_enum.value).encode(), "text/plain")

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, json.dumps(prop.to_dict()).encode(), "application/json")

        field_dict.update(
            {
                "some_file": some_file,
                "some_object": some_object,
                "some_nullable_object": some_nullable_object,
            }
        )
        if some_optional_file is not UNSET:
            field_dict["some_optional_file"] = some_optional_file
        if some_string is not UNSET:
            field_dict["some_string"] = some_string
        if a_datetime is not UNSET:
            field_dict["a_datetime"] = a_datetime
        if a_date is not UNSET:
            field_dict["a_date"] = a_date
        if some_number is not UNSET:
            field_dict["some_number"] = some_number
        if some_array is not UNSET:
            field_dict["some_array"] = some_array
        if some_optional_object is not UNSET:
            field_dict["some_optional_object"] = some_optional_object
        if some_enum is not UNSET:
            field_dict["some_enum"] = some_enum

        return field_dict

    @classmethod
    def from_dict(cls: Type[BodyUploadFileTestsUploadPost], src_dict: Dict[str, Any]) -> BodyUploadFileTestsUploadPost:
        d = src_dict.copy()
        some_file = File(payload=BytesIO(d.pop("some_file")))

        some_object = BodyUploadFileTestsUploadPostSomeObject.from_dict(d.pop("some_object"))

        _some_optional_file = d.pop("some_optional_file", UNSET)
        some_optional_file: Union[Unset, File]
        if isinstance(_some_optional_file, Unset):
            some_optional_file = UNSET
        else:
            some_optional_file = File(payload=BytesIO(_some_optional_file))

        some_string = d.pop("some_string", UNSET)

        _a_datetime = d.pop("a_datetime", UNSET)
        a_datetime: Union[Unset, datetime.datetime]
        if isinstance(_a_datetime, Unset):
            a_datetime = UNSET
        else:
            a_datetime = isoparse(_a_datetime)

        _a_date = d.pop("a_date", UNSET)
        a_date: Union[Unset, datetime.date]
        if isinstance(_a_date, Unset):
            a_date = UNSET
        else:
            a_date = isoparse(_a_date).date()

        some_number = d.pop("some_number", UNSET)

        some_array = cast(List[float], d.pop("some_array", UNSET))

        _some_optional_object = d.pop("some_optional_object", UNSET)
        some_optional_object: Union[Unset, BodyUploadFileTestsUploadPostSomeOptionalObject]
        if isinstance(_some_optional_object, Unset):
            some_optional_object = UNSET
        else:
            some_optional_object = BodyUploadFileTestsUploadPostSomeOptionalObject.from_dict(_some_optional_object)

        _some_nullable_object = d.pop("some_nullable_object")
        some_nullable_object: Optional[BodyUploadFileTestsUploadPostSomeNullableObject]
        if _some_nullable_object is None:
            some_nullable_object = None
        else:
            some_nullable_object = BodyUploadFileTestsUploadPostSomeNullableObject.from_dict(_some_nullable_object)

        _some_enum = d.pop("some_enum", UNSET)
        some_enum: Union[Unset, DifferentEnum]
        if isinstance(_some_enum, Unset):
            some_enum = UNSET
        else:
            some_enum = DifferentEnum(_some_enum)

        body_upload_file_tests_upload_post = cls(
            some_file=some_file,
            some_object=some_object,
            some_optional_file=some_optional_file,
            some_string=some_string,
            a_datetime=a_datetime,
            a_date=a_date,
            some_number=some_number,
            some_array=some_array,
            some_optional_object=some_optional_object,
            some_nullable_object=some_nullable_object,
            some_enum=some_enum,
        )

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = BodyUploadFileTestsUploadPostAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        body_upload_file_tests_upload_post.additional_properties = additional_properties
        return body_upload_file_tests_upload_post

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> BodyUploadFileTestsUploadPostAdditionalProperty:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: BodyUploadFileTestsUploadPostAdditionalProperty) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties


@attr.s(auto_attribs=True)
class HTTPValidationError:
    """
    Attributes:
        detail (Union[Unset, List[ValidationError]]):
    """

    detail: Union[Unset, List[ValidationError]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        detail: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.detail, Unset):
            detail = []
            for detail_item_data in self.detail:
                detail_item = detail_item_data.to_dict()

                detail.append(detail_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if detail is not UNSET:
            field_dict["detail"] = detail

        return field_dict

    @classmethod
    def from_dict(cls: Type[HTTPValidationError], src_dict: Dict[str, Any]) -> HTTPValidationError:
        d = src_dict.copy()
        detail = []
        _detail = d.pop("detail", UNSET)
        for detail_item_data in _detail or []:
            detail_item = ValidationError.from_dict(detail_item_data)

            detail.append(detail_item)

        http_validation_error = cls(
            detail=detail,
        )

        return http_validation_error


@attr.s(auto_attribs=True)
class ModelFromAllOf:
    """
    Attributes:
        a_sub_property (Union[Unset, str]):
        type (Union[Unset, AnotherAllOfSubModelType]):
        type_enum (Union[Unset, AnotherAllOfSubModelTypeEnum]):
        another_sub_property (Union[Unset, str]):
    """

    a_sub_property: Union[Unset, str] = UNSET
    type: Union[Unset, AnotherAllOfSubModelType] = UNSET
    type_enum: Union[Unset, AnotherAllOfSubModelTypeEnum] = UNSET
    another_sub_property: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        a_sub_property = self.a_sub_property
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        type_enum: Union[Unset, int] = UNSET
        if not isinstance(self.type_enum, Unset):
            type_enum = self.type_enum.value

        another_sub_property = self.another_sub_property

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if a_sub_property is not UNSET:
            field_dict["a_sub_property"] = a_sub_property
        if type is not UNSET:
            field_dict["type"] = type
        if type_enum is not UNSET:
            field_dict["type_enum"] = type_enum
        if another_sub_property is not UNSET:
            field_dict["another_sub_property"] = another_sub_property

        return field_dict

    @classmethod
    def from_dict(cls: Type[ModelFromAllOf], src_dict: Dict[str, Any]) -> ModelFromAllOf:
        d = src_dict.copy()
        a_sub_property = d.pop("a_sub_property", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, AnotherAllOfSubModelType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = AnotherAllOfSubModelType(_type)

        _type_enum = d.pop("type_enum", UNSET)
        type_enum: Union[Unset, AnotherAllOfSubModelTypeEnum]
        if isinstance(_type_enum, Unset):
            type_enum = UNSET
        else:
            type_enum = AnotherAllOfSubModelTypeEnum(_type_enum)

        another_sub_property = d.pop("another_sub_property", UNSET)

        model_from_all_of = cls(
            a_sub_property=a_sub_property,
            type=type,
            type_enum=type_enum,
            another_sub_property=another_sub_property,
        )

        model_from_all_of.additional_properties = d
        return model_from_all_of

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


@attr.s(auto_attribs=True)
class AModelWithPropertiesReferenceThatAreNotObject:
    """
    Attributes:
        enum_properties_ref (List[AnEnum]):
        str_properties_ref (List[str]):
        date_properties_ref (List[datetime.date]):
        datetime_properties_ref (List[datetime.datetime]):
        int32_properties_ref (List[int]):
        int64_properties_ref (List[int]):
        float_properties_ref (List[float]):
        double_properties_ref (List[float]):
        file_properties_ref (List[File]):
        bytestream_properties_ref (List[str]):
        enum_properties (List[AnEnum]):
        str_properties (List[str]):
        date_properties (List[datetime.date]):
        datetime_properties (List[datetime.datetime]):
        int32_properties (List[int]):
        int64_properties (List[int]):
        float_properties (List[float]):
        double_properties (List[float]):
        file_properties (List[File]):
        bytestream_properties (List[str]):
        enum_property_ref (AnEnum): For testing Enums in all the ways they can be used
        str_property_ref (str):
        date_property_ref (datetime.date):
        datetime_property_ref (datetime.datetime):
        int32_property_ref (int):
        int64_property_ref (int):
        float_property_ref (float):
        double_property_ref (float):
        file_property_ref (File):
        bytestream_property_ref (str):
    """

    enum_properties_ref: List[AnEnum]
    str_properties_ref: List[str]
    date_properties_ref: List[datetime.date]
    datetime_properties_ref: List[datetime.datetime]
    int32_properties_ref: List[int]
    int64_properties_ref: List[int]
    float_properties_ref: List[float]
    double_properties_ref: List[float]
    file_properties_ref: List[File]
    bytestream_properties_ref: List[str]
    enum_properties: List[AnEnum]
    str_properties: List[str]
    date_properties: List[datetime.date]
    datetime_properties: List[datetime.datetime]
    int32_properties: List[int]
    int64_properties: List[int]
    float_properties: List[float]
    double_properties: List[float]
    file_properties: List[File]
    bytestream_properties: List[str]
    enum_property_ref: AnEnum
    str_property_ref: str
    date_property_ref: datetime.date
    datetime_property_ref: datetime.datetime
    int32_property_ref: int
    int64_property_ref: int
    float_property_ref: float
    double_property_ref: float
    file_property_ref: File
    bytestream_property_ref: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        enum_properties_ref = []
        for componentsschemas_an_other_array_of_enum_item_data in self.enum_properties_ref:
            componentsschemas_an_other_array_of_enum_item = componentsschemas_an_other_array_of_enum_item_data.value

            enum_properties_ref.append(componentsschemas_an_other_array_of_enum_item)

        str_properties_ref = self.str_properties_ref

        date_properties_ref = []
        for componentsschemas_an_other_array_of_date_item_data in self.date_properties_ref:
            componentsschemas_an_other_array_of_date_item = (
                componentsschemas_an_other_array_of_date_item_data.isoformat()
            )
            date_properties_ref.append(componentsschemas_an_other_array_of_date_item)

        datetime_properties_ref = []
        for componentsschemas_an_other_array_of_date_time_item_data in self.datetime_properties_ref:
            componentsschemas_an_other_array_of_date_time_item = (
                componentsschemas_an_other_array_of_date_time_item_data.isoformat()
            )

            datetime_properties_ref.append(componentsschemas_an_other_array_of_date_time_item)

        int32_properties_ref = self.int32_properties_ref

        int64_properties_ref = self.int64_properties_ref

        float_properties_ref = self.float_properties_ref

        double_properties_ref = self.double_properties_ref

        file_properties_ref = []
        for componentsschemas_an_other_array_of_file_item_data in self.file_properties_ref:
            componentsschemas_an_other_array_of_file_item = (
                componentsschemas_an_other_array_of_file_item_data.to_tuple()
            )

            file_properties_ref.append(componentsschemas_an_other_array_of_file_item)

        bytestream_properties_ref = self.bytestream_properties_ref

        enum_properties = []
        for componentsschemas_an_array_of_enum_item_data in self.enum_properties:
            componentsschemas_an_array_of_enum_item = componentsschemas_an_array_of_enum_item_data.value

            enum_properties.append(componentsschemas_an_array_of_enum_item)

        str_properties = self.str_properties

        date_properties = []
        for componentsschemas_an_array_of_date_item_data in self.date_properties:
            componentsschemas_an_array_of_date_item = componentsschemas_an_array_of_date_item_data.isoformat()
            date_properties.append(componentsschemas_an_array_of_date_item)

        datetime_properties = []
        for componentsschemas_an_array_of_date_time_item_data in self.datetime_properties:
            componentsschemas_an_array_of_date_time_item = componentsschemas_an_array_of_date_time_item_data.isoformat()

            datetime_properties.append(componentsschemas_an_array_of_date_time_item)

        int32_properties = self.int32_properties

        int64_properties = self.int64_properties

        float_properties = self.float_properties

        double_properties = self.double_properties

        file_properties = []
        for componentsschemas_an_array_of_file_item_data in self.file_properties:
            componentsschemas_an_array_of_file_item = componentsschemas_an_array_of_file_item_data.to_tuple()

            file_properties.append(componentsschemas_an_array_of_file_item)

        bytestream_properties = self.bytestream_properties

        enum_property_ref = self.enum_property_ref.value

        str_property_ref = self.str_property_ref
        date_property_ref = self.date_property_ref.isoformat()
        datetime_property_ref = self.datetime_property_ref.isoformat()

        int32_property_ref = self.int32_property_ref
        int64_property_ref = self.int64_property_ref
        float_property_ref = self.float_property_ref
        double_property_ref = self.double_property_ref
        file_property_ref = self.file_property_ref.to_tuple()

        bytestream_property_ref = self.bytestream_property_ref

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "enum_properties_ref": enum_properties_ref,
                "str_properties_ref": str_properties_ref,
                "date_properties_ref": date_properties_ref,
                "datetime_properties_ref": datetime_properties_ref,
                "int32_properties_ref": int32_properties_ref,
                "int64_properties_ref": int64_properties_ref,
                "float_properties_ref": float_properties_ref,
                "double_properties_ref": double_properties_ref,
                "file_properties_ref": file_properties_ref,
                "bytestream_properties_ref": bytestream_properties_ref,
                "enum_properties": enum_properties,
                "str_properties": str_properties,
                "date_properties": date_properties,
                "datetime_properties": datetime_properties,
                "int32_properties": int32_properties,
                "int64_properties": int64_properties,
                "float_properties": float_properties,
                "double_properties": double_properties,
                "file_properties": file_properties,
                "bytestream_properties": bytestream_properties,
                "enum_property_ref": enum_property_ref,
                "str_property_ref": str_property_ref,
                "date_property_ref": date_property_ref,
                "datetime_property_ref": datetime_property_ref,
                "int32_property_ref": int32_property_ref,
                "int64_property_ref": int64_property_ref,
                "float_property_ref": float_property_ref,
                "double_property_ref": double_property_ref,
                "file_property_ref": file_property_ref,
                "bytestream_property_ref": bytestream_property_ref,
            }
        )

        return field_dict

    @classmethod
    def from_dict(
        cls: Type[AModelWithPropertiesReferenceThatAreNotObject], src_dict: Dict[str, Any]
    ) -> AModelWithPropertiesReferenceThatAreNotObject:
        d = src_dict.copy()
        enum_properties_ref = []
        _enum_properties_ref = d.pop("enum_properties_ref")
        for componentsschemas_an_other_array_of_enum_item_data in _enum_properties_ref:
            componentsschemas_an_other_array_of_enum_item = AnEnum(componentsschemas_an_other_array_of_enum_item_data)

            enum_properties_ref.append(componentsschemas_an_other_array_of_enum_item)

        str_properties_ref = cast(List[str], d.pop("str_properties_ref"))

        date_properties_ref = []
        _date_properties_ref = d.pop("date_properties_ref")
        for componentsschemas_an_other_array_of_date_item_data in _date_properties_ref:
            componentsschemas_an_other_array_of_date_item = isoparse(
                componentsschemas_an_other_array_of_date_item_data
            ).date()

            date_properties_ref.append(componentsschemas_an_other_array_of_date_item)

        datetime_properties_ref = []
        _datetime_properties_ref = d.pop("datetime_properties_ref")
        for componentsschemas_an_other_array_of_date_time_item_data in _datetime_properties_ref:
            componentsschemas_an_other_array_of_date_time_item = isoparse(
                componentsschemas_an_other_array_of_date_time_item_data
            )

            datetime_properties_ref.append(componentsschemas_an_other_array_of_date_time_item)

        int32_properties_ref = cast(List[int], d.pop("int32_properties_ref"))

        int64_properties_ref = cast(List[int], d.pop("int64_properties_ref"))

        float_properties_ref = cast(List[float], d.pop("float_properties_ref"))

        double_properties_ref = cast(List[float], d.pop("double_properties_ref"))

        file_properties_ref = []
        _file_properties_ref = d.pop("file_properties_ref")
        for componentsschemas_an_other_array_of_file_item_data in _file_properties_ref:
            componentsschemas_an_other_array_of_file_item = File(
                payload=BytesIO(componentsschemas_an_other_array_of_file_item_data)
            )

            file_properties_ref.append(componentsschemas_an_other_array_of_file_item)

        bytestream_properties_ref = cast(List[str], d.pop("bytestream_properties_ref"))

        enum_properties = []
        _enum_properties = d.pop("enum_properties")
        for componentsschemas_an_array_of_enum_item_data in _enum_properties:
            componentsschemas_an_array_of_enum_item = AnEnum(componentsschemas_an_array_of_enum_item_data)

            enum_properties.append(componentsschemas_an_array_of_enum_item)

        str_properties = cast(List[str], d.pop("str_properties"))

        date_properties = []
        _date_properties = d.pop("date_properties")
        for componentsschemas_an_array_of_date_item_data in _date_properties:
            componentsschemas_an_array_of_date_item = isoparse(componentsschemas_an_array_of_date_item_data).date()

            date_properties.append(componentsschemas_an_array_of_date_item)

        datetime_properties = []
        _datetime_properties = d.pop("datetime_properties")
        for componentsschemas_an_array_of_date_time_item_data in _datetime_properties:
            componentsschemas_an_array_of_date_time_item = isoparse(componentsschemas_an_array_of_date_time_item_data)

            datetime_properties.append(componentsschemas_an_array_of_date_time_item)

        int32_properties = cast(List[int], d.pop("int32_properties"))

        int64_properties = cast(List[int], d.pop("int64_properties"))

        float_properties = cast(List[float], d.pop("float_properties"))

        double_properties = cast(List[float], d.pop("double_properties"))

        file_properties = []
        _file_properties = d.pop("file_properties")
        for componentsschemas_an_array_of_file_item_data in _file_properties:
            componentsschemas_an_array_of_file_item = File(
                payload=BytesIO(componentsschemas_an_array_of_file_item_data)
            )

            file_properties.append(componentsschemas_an_array_of_file_item)

        bytestream_properties = cast(List[str], d.pop("bytestream_properties"))

        enum_property_ref = AnEnum(d.pop("enum_property_ref"))

        str_property_ref = d.pop("str_property_ref")

        date_property_ref = isoparse(d.pop("date_property_ref")).date()

        datetime_property_ref = isoparse(d.pop("datetime_property_ref"))

        int32_property_ref = d.pop("int32_property_ref")

        int64_property_ref = d.pop("int64_property_ref")

        float_property_ref = d.pop("float_property_ref")

        double_property_ref = d.pop("double_property_ref")

        file_property_ref = File(payload=BytesIO(d.pop("file_property_ref")))

        bytestream_property_ref = d.pop("bytestream_property_ref")

        a_model_with_properties_reference_that_are_not_object = cls(
            enum_properties_ref=enum_properties_ref,
            str_properties_ref=str_properties_ref,
            date_properties_ref=date_properties_ref,
            datetime_properties_ref=datetime_properties_ref,
            int32_properties_ref=int32_properties_ref,
            int64_properties_ref=int64_properties_ref,
            float_properties_ref=float_properties_ref,
            double_properties_ref=double_properties_ref,
            file_properties_ref=file_properties_ref,
            bytestream_properties_ref=bytestream_properties_ref,
            enum_properties=enum_properties,
            str_properties=str_properties,
            date_properties=date_properties,
            datetime_properties=datetime_properties,
            int32_properties=int32_properties,
            int64_properties=int64_properties,
            float_properties=float_properties,
            double_properties=double_properties,
            file_properties=file_properties,
            bytestream_properties=bytestream_properties,
            enum_property_ref=enum_property_ref,
            str_property_ref=str_property_ref,
            date_property_ref=date_property_ref,
            datetime_property_ref=datetime_property_ref,
            int32_property_ref=int32_property_ref,
            int64_property_ref=int64_property_ref,
            float_property_ref=float_property_ref,
            double_property_ref=double_property_ref,
            file_property_ref=file_property_ref,
            bytestream_property_ref=bytestream_property_ref,
        )

        a_model_with_properties_reference_that_are_not_object.additional_properties = d
        return a_model_with_properties_reference_that_are_not_object

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


@attr.s(auto_attribs=True)
class TestInlineObjectsResponse200:
    """
    Attributes:
        a_property (Union[Unset, str]):
    """

    a_property: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        a_property = self.a_property

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if a_property is not UNSET:
            field_dict["a_property"] = a_property

        return field_dict

    @classmethod
    def from_dict(cls: Type[TestInlineObjectsResponse200], src_dict: Dict[str, Any]) -> TestInlineObjectsResponse200:
        d = src_dict.copy()
        a_property = d.pop("a_property", UNSET)

        test_inline_objects_response_200 = cls(
            a_property=a_property,
        )

        return test_inline_objects_response_200


@attr.s(auto_attribs=True)
class TestInlineObjectsJsonBody:
    """
    Attributes:
        a_property (Union[Unset, str]):
    """

    a_property: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        a_property = self.a_property

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if a_property is not UNSET:
            field_dict["a_property"] = a_property

        return field_dict

    @classmethod
    def from_dict(cls: Type[TestInlineObjectsJsonBody], src_dict: Dict[str, Any]) -> TestInlineObjectsJsonBody:
        d = src_dict.copy()
        a_property = d.pop("a_property", UNSET)

        test_inline_objects_json_body = cls(
            a_property=a_property,
        )

        return test_inline_objects_json_body
