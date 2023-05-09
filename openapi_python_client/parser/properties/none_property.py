from typing import ClassVar

import attr

from .property import Property


@attr.s(auto_attribs=True, frozen=True)
class NoneProperty(Property):
    """A property that can only be None"""

    _type_string: ClassVar[str] = "None"
    _json_type_string: ClassVar[str] = "None"
