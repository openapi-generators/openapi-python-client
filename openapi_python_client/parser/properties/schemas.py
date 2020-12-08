__all__ = ["Schemas"]

from typing import Dict, List

import attr

from ..errors import ParseError

# Avoid circular import with forward reference
from . import model_property
from .enum_property import EnumProperty


@attr.s(auto_attribs=True, frozen=True)
class Schemas:
    """ Structure for containing all defined, shareable, and resuabled schemas (attr classes and Enums) """

    enums: Dict[str, EnumProperty] = attr.ib(factory=dict)
    models: Dict[str, "model_property.ModelProperty"] = attr.ib(factory=dict)
    errors: List[ParseError] = attr.ib(factory=list)
