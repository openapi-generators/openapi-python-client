""" Contains some shared types for properties """
from dataclasses import dataclass
from typing import BinaryIO, Optional, TextIO, Tuple, Union


@dataclass
class File:
    """ Contains information for file uploads """

    payload: Union[BinaryIO, TextIO]
    file_name: Optional[str] = None
    mime_type: Optional[str] = None

    def to_tuple(self) -> Tuple[Optional[str], Union[BinaryIO, TextIO], Optional[str]]:
        """ Return a tuple representation that httpx will accept for multipart/form-data """
        return self.file_name, self.payload, self.mime_type


__all__ = ["File"]
