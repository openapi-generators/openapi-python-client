__all__ = ["Schemas"]

from typing import Dict, List

import attr

from ..errors import ParseError
from .enum_property import EnumProperty
from .model_property import ModelProperty


@attr.s(auto_attribs=True, frozen=True)
class Schemas:
    """ Structure for containing all defined, shareable, and resuabled schemas (attr classes and Enums) """

    enums: Dict[str, EnumProperty] = attr.ib(factory=dict)
    models: Dict[str, ModelProperty] = attr.ib(factory=dict)
    errors: List[ParseError] = attr.ib(factory=list)
