from dataclasses import dataclass

from ..schema.openapi_schema_pydantic.security_scheme import SecurityScheme as _SecurityScheme
from ..utils import ClassName


@dataclass
class SecurityScheme:
    scheme: _SecurityScheme
    name: str
    class_name: ClassName
