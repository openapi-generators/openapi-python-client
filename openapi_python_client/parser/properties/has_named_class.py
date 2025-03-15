from typing import Protocol, runtime_checkable

from .schemas import Class


@runtime_checkable
class HasNamedClass(Protocol):
    class_info: Class
