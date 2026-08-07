__all__ = ["Property"]


from typing import TypeAlias

from .any import AnyProperty
from .boolean import BooleanProperty
from .branded_string import BrandedStringProperty
from .const import ConstProperty
from .date import DateProperty
from .datetime import DateTimeProperty
from .dict_property import DictProperty
from .enum_property import EnumProperty
from .file import FileProperty
from .float import FloatProperty
from .int import IntProperty
from .jsonl_property import JsonlProperty
from .list_property import ListProperty
from .literal_enum_property import LiteralEnumProperty
from .model_property import ModelProperty
from .none import NoneProperty
from .string import StringProperty
from .union import UnionProperty
from .uuid import UuidProperty

Property: TypeAlias = (
    AnyProperty
    | BooleanProperty
    | BrandedStringProperty
    | ConstProperty
    | DateProperty
    | DateTimeProperty
    | DictProperty
    | EnumProperty
    | LiteralEnumProperty
    | FileProperty
    | FloatProperty
    | IntProperty
    | JsonlProperty
    | ListProperty
    | ModelProperty
    | NoneProperty
    | StringProperty
    | UnionProperty
    | UuidProperty
)
