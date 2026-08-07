"""Contains all the data models used in inputs/outputs"""

from .an_object import AnObject
from .file import File
from .post_body_multipart_body import PostBodyMultipartBody
from .post_body_multipart_response_200 import PostBodyMultipartResponse200
from .post_parameters_header_response_200 import PostParametersHeaderResponse200
from .problem import Problem
from .public_error import PublicError

__all__ = (
    "AnObject",
    "File",
    "PostBodyMultipartBody",
    "PostBodyMultipartResponse200",
    "PostParametersHeaderResponse200",
    "Problem",
    "PublicError",
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
