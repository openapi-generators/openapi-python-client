"""Contains all the data models used in inputs/outputs"""

from .post_const_path_body import PostConstPathBody
from .post_prefix_items_body import PostPrefixItemsBody
from .post_upload_body import PostUploadBody

__all__ = (
    "PostConstPathBody",
    "PostPrefixItemsBody",
    "PostUploadBody",
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
