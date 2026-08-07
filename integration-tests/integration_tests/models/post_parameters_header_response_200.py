from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from pydantic import ConfigDict
from tandem_platform.schema.protected import BaseModel

T = TypeVar("T", bound="PostParametersHeaderResponse200")


class PostParametersHeaderResponse200(BaseModel):
    """
    Attributes:
        boolean (bool): Echo of the 'Boolean-Header' input parameter from the header.
        string (str): Echo of the 'String-Header' input parameter from the header.
        number (float): Echo of the 'Number-Header' input parameter from the header.
        integer (int): Echo of the 'Integer-Header' input parameter from the header.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    boolean: bool
    string: str
    number: float
    integer: int

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        return cls.model_validate(src_dict)
