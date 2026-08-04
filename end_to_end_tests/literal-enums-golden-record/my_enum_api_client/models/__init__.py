"""Contains all the data models used in inputs/outputs"""

from .a_model import AModel
from .an_all_of_enum import AnAllOfEnum
from .an_enum import AnEnum
from .an_enum_with_null import AnEnumWithNull
from .an_int_enum import AnIntEnum
from .different_enum import DifferentEnum
from .get_user_list_int_enum_header import GetUserListIntEnumHeader
from .get_user_list_string_enum_header import GetUserListStringEnumHeader
from .post_user_list_body import PostUserListBody

__all__ = (
    "AModel",
    "AnAllOfEnum",
    "AnEnum",
    "AnEnumWithNull",
    "AnIntEnum",
    "DifferentEnum",
    "GetUserListIntEnumHeader",
    "GetUserListStringEnumHeader",
    "PostUserListBody",
)


def _rebuild_cyclic_models() -> None:
    # models in import cycles defer their rebuild
    # (model.py.jinja passes raise_errors=False); finish them here now that
    # every model module is imported.
    from pydantic import BaseModel

    for _name in __all__:
        _obj = globals()[_name]
        if isinstance(_obj, type) and issubclass(_obj, BaseModel):
            if not _obj.__pydantic_complete__:
                _obj.model_rebuild()


_rebuild_cyclic_models()
