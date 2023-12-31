__all__ = ["Property"]

from typing import Union

from typing_extensions import TypeAlias

from .any import AnyProperty
from .boolean import BooleanProperty
from .const import ConstProperty
from .date import DateProperty
from .datetime import DateTimeProperty
from .enum_property import EnumProperty
from .file import FileProperty
from .float import FloatProperty
from .int import IntProperty
from .list_property import ListProperty
from .model_property import ModelProperty
from .none import NoneProperty
from .string import StringProperty
from .union import UnionProperty

Property: TypeAlias = Union[
    AnyProperty,
    BooleanProperty,
    ConstProperty,
    DateProperty,
    DateTimeProperty,
    EnumProperty,
    FileProperty,
    FloatProperty,
    IntProperty,
    ListProperty,
    ModelProperty,
    NoneProperty,
    StringProperty,
    UnionProperty,
]
