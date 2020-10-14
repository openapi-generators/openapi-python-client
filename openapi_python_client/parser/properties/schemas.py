__all__ = ["Schemas"]

from dataclasses import dataclass, field
from typing import Dict, List

from ..errors import ParseError
from .enum_property import EnumProperty
from .model_property import ModelProperty


@dataclass
class Schemas:
    """ Structure for containing all defined, shareable, and resuabled schemas (attr classes and Enums) """

    enums: Dict[str, EnumProperty] = field(default_factory=dict)
    models: Dict[str, ModelProperty] = field(default_factory=dict)
    errors: List[ParseError] = field(default_factory=list)
