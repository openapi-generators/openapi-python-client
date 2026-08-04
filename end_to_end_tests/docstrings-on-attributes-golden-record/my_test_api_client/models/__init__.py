"""Contains all the data models used in inputs/outputs"""

from .model_with_description import ModelWithDescription
from .model_with_no_description import ModelWithNoDescription

__all__ = (
    "ModelWithDescription",
    "ModelWithNoDescription",
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
