from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

__all__ = ["ErrorLevel", "GeneratorError", "ParseError", "PropertyError", "ValidationError"]

from pydantic import BaseModel


class ErrorLevel(Enum):
    """The level of an error"""

    WARNING = "WARNING"  # Client is still generated but missing some pieces
    ERROR = "ERROR"  # Client could not be generated


@dataclass
class GeneratorError:
    """Base data struct containing info on an error that occurred"""

    detail: Optional[str] = None
    level: ErrorLevel = ErrorLevel.ERROR
    header: str = "Unable to generate the client"


@dataclass
class ParseError(GeneratorError):
    """An error raised when there's a problem parsing an OpenAPI document"""

    level: ErrorLevel = ErrorLevel.WARNING
    data: Optional[BaseModel] = None
    header: str = "Unable to parse this part of your OpenAPI document: "


@dataclass
class PropertyError(ParseError):
    """Error raised when there's a problem creating a Property"""

    header = "Problem creating a Property: "


@dataclass
class RecursiveReferenceInterupt(PropertyError):
    """Error raised when a property have an recursive reference to itself"""

    schemas: Optional[Any] = None  # TODO: shall not use Any here, shall be Schemas, to fix later


class ValidationError(Exception):
    pass
