from typing import Any, TypeVar

from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema

T = TypeVar("T")


class UntrustedString:
    """A raw string in the OpenAPI document which should not be directly placed in the generated code."""

    def __init__(self, value: str) -> None:
        self._value = value

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: GetCoreSchemaHandler) -> CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls,
            core_schema.str_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                cls._serialize, info_arg=True, return_schema=core_schema.any_schema()
            ),
        )

    @staticmethod
    def _serialize(value: "UntrustedString", info: core_schema.SerializationInfo) -> Any:
        # Only unwrap in JSON mode (used for error messages); Python mode keeps the wrapper so it
        # can't leak into generated code. Returning the wrapper also avoids serializer warnings.
        if info.mode == "json":
            return value.get_untrusted_value()
        return value

    def get_untrusted_value(self) -> str:
        """
        Return the raw string with no transformations.

        DO NOT use this for generating code directly. It can result in arbitrary code generation.
        """
        return self._value

    def startswith(self, prefix: str) -> bool:
        return self._value.startswith(prefix)

    def __bool__(self) -> bool:
        """Whether the raw value is non-empty. Emptiness is not sensitive, so this is safe to expose."""
        return bool(self._value)

    def __hash__(self) -> int:
        return hash(self._value)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, UntrustedString):
            return self._value == other._value
        if isinstance(other, str):
            return self._value == other
        return False
