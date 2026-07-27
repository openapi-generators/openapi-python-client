"""Contains some shared types for properties"""

from collections.abc import Mapping, MutableMapping
from http import HTTPStatus
from io import BytesIO
from typing import IO, Any, BinaryIO, Generic, Literal, TypeVar

from attrs import define
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema


class Unset:
    def __bool__(self) -> Literal[False]:
        return False


UNSET: Unset = Unset()

# The types that `httpx.Client(files=)` can accept, copied from that library.
FileContent = IO[bytes] | bytes | str
FileTypes = (
    # (filename, file (or bytes), content_type)
    tuple[str | None, FileContent, str | None]
    # (filename, file (or bytes), content_type, headers)
    | tuple[str | None, FileContent, str | None, Mapping[str, str]]
)
RequestFiles = list[tuple[str, FileTypes]]


@define
class File:
    """Contains information for file uploads"""

    payload: BinaryIO
    file_name: str | None = None
    mime_type: str | None = None

    def to_tuple(self) -> FileTypes:
        """Return a tuple representation that httpx will accept for multipart/form-data"""
        return self.file_name, self.payload, self.mime_type

    @classmethod
    def _validate(cls, value: Any) -> "File":
        if isinstance(value, File):
            return value
        if isinstance(value, (bytes, bytearray)):
            return cls(payload=BytesIO(bytes(value)))
        if hasattr(value, "read"):
            return cls(payload=value)
        raise ValueError(f"expected a File or binary data, got {type(value).__name__}")

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        """Teach Pydantic how to handle a File field.

        `payload` is an arbitrary binary stream that Pydantic cannot introspect. Without
        this hook, every model holding a binary property -- a multipart request body, an
        octet-stream response, a list of uploads -- fails to build its schema and the
        module raises `PydanticSchemaGenerationError` on import.

        An existing File passes through untouched: re-wrapping it would detach the
        caller's stream, and copying it would re-read one that may already be consumed.
        """
        return core_schema.no_info_plain_validator_function(
            cls._validate,
            serialization=core_schema.plain_serializer_function_ser_schema(
                cls._serialize, info_arg=True, return_schema=core_schema.any_schema()
            ),
        )

    @staticmethod
    def _serialize(value: "File", info: core_schema.SerializationInfo) -> Any:
        # JSON mode emits metadata only. The payload has no faithful JSON form, and
        # letting Pydantic fall back to inference would drain the stream -- usually the
        # very stream that is about to be uploaded.
        if info.mode == "json":
            return {"file_name": value.file_name, "mime_type": value.mime_type}
        # Python mode hands the File back untouched, as `model_dump` does for any
        # non-Pydantic value.
        return value


T = TypeVar("T")


@define
class Response(Generic[T]):
    """A response from an endpoint"""

    status_code: HTTPStatus
    content: bytes
    headers: MutableMapping[str, str]
    parsed: T


__all__ = ["UNSET", "File", "FileTypes", "RequestFiles", "Response", "Unset"]
