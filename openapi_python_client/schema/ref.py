from typing import Any

from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema

from .untrusted_string import UntrustedString


class Ref:
    """A $ref in the schema, the raw value is protected to make sure we don't accidentally place it in the generated code."""

    def __init__(self, value: str | UntrustedString) -> None:
        if isinstance(value, UntrustedString):
            value = value.get_untrusted_value()
        self._value = value

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls,
            core_schema.str_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                cls._serialize, info_arg=True, return_schema=core_schema.any_schema()
            ),
        )

    @staticmethod
    def _serialize(value: "Ref", info: core_schema.SerializationInfo) -> Any:
        # Only unwrap in JSON mode (used for error messages); Python mode keeps the wrapper so it
        # can't leak into generated code. Returning the wrapper also avoids serializer warnings.
        if info.mode == "json":
            return value.get_untrusted_value()
        return value

    def get_untrusted_value(self) -> str:
        """
        Get the raw $ref value.

        DO NOT place this in generated code.
        """
        return self._value

    def endswith(self, suffix: str) -> bool:
        return self._value.endswith(suffix)

    def __hash__(self) -> int:
        return hash(self._value)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Ref):
            return self._value == other._value
        return False  # pragma: no cover
