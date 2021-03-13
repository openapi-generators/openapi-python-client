__all__ = ["Schemas"]

from typing import TYPE_CHECKING, Dict, List

import attr

from ..errors import ParseError

if TYPE_CHECKING:  # pragma: no cover
    from .enum_property import EnumProperty
    from .model_property import ModelProperty
else:
    EnumProperty = "EnumProperty"
    ModelProperty = "ModelProperty"


@attr.s(auto_attribs=True, frozen=True)
class Schemas:
    """ Structure for containing all defined, shareable, and resuabled schemas (attr classes and Enums) """

    enums: Dict[str, EnumProperty] = attr.ib(factory=dict)
    models: Dict[str, ModelProperty] = attr.ib(factory=dict)
    errors: List[ParseError] = attr.ib(factory=list)
