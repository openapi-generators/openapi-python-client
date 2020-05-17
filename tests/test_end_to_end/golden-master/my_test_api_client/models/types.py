""" Contains some shared types for properties """
from dataclasses import dataclass
from typing import IO, Optional, Tuple


@dataclass
class File:
    """ Contains information for file uploads """

    payload: IO
    file_name: Optional[str] = None
    mime_type: Optional[str] = None

    def to_tuple(self) -> Tuple[Optional[str], IO, Optional[str]]:
        """ Return a tuple representation that httpx will accept for multipart/form-data """
        return self.file_name, self.payload, self.mime_type


__all__ = ["File"]
