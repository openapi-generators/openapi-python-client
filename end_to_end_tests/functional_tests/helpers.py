from typing import Any, Dict
import asyncio
import importlib
import re

import httpx
from typer.testing import Result
import pytest

from end_to_end_tests.generated_client import generate_client_from_inline_spec, GeneratedClientContext


def mock_client(
    Client: Any,
    *,
    status_code: int = 200,
    json: Any = None,
    content: bytes | None = None,
    lines: list[str] | None = None,
    **client_kwargs: Any,
) -> Any:
    """Build a generated Client whose async httpx client answers every request the same way.

    A real `httpx.AsyncClient` over a `MockTransport` rather than a `MagicMock`, so the generated code's
    `aread()`/`json()`/`text`/`aiter_lines()` all behave as they would against a live server -- which matters for the
    streaming endpoints, where the error path reads a response it was streaming.

    `lines` builds a JSONL body; pass the lines already serialized.
    """

    def handler(request: httpx.Request) -> httpx.Response:
        if lines is not None:
            return httpx.Response(status_code, content="\n".join(lines).encode())
        if content is not None:
            return httpx.Response(status_code, content=content)
        if json is None:
            return httpx.Response(status_code)
        return httpx.Response(status_code, json=json)

    client = Client(base_url="https://example.com", **client_kwargs)
    client.set_async_httpx_client(
        httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://example.com")
    )
    return client


def call(
    Client: Any,
    endpoint: Any,
    *,
    status_code: int = 200,
    json: Any = None,
    content: bytes | None = None,
    **kwargs: Any,
) -> Any:
    """Call a generated async endpoint function against a canned response.

    `json=None` means "no body at all", so pass `content=b"null"` to send a literal JSON `null`.
    """
    client_kwargs = {}
    if "raise_on_unexpected_status" in kwargs:
        client_kwargs["raise_on_unexpected_status"] = kwargs.pop("raise_on_unexpected_status")
    client = mock_client(Client, status_code=status_code, json=json, content=content, **client_kwargs)
    return asyncio.run(endpoint(client=client, **kwargs))


def call_recording_requests(
    Client: Any,
    endpoint: Any,
    *,
    status_code: int = 200,
    json: Any = None,
    **kwargs: Any,
) -> list[httpx.Request]:
    """Call a generated async endpoint and return the requests it issued.

    For assertions about how the request was *built* -- URL encoding, headers, body -- rather than about
    how the response was parsed. Recording the `httpx.Request` rather than the kwargs handed to
    `httpx.request()` means the assertion covers httpx's own URL handling too, so it holds for what
    actually goes on the wire.
    """
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if json is None:
            return httpx.Response(status_code)
        return httpx.Response(status_code, json=json)

    client = Client(base_url="https://example.com")
    client.set_async_httpx_client(
        httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://example.com")
    )
    asyncio.run(endpoint(client=client, **kwargs))
    return requests


def drain(Client: Any, stream_endpoint: Any, **mock_client_kwargs: Any) -> list[Any]:
    """Consume a generated `stream` endpoint to exhaustion and return everything it yielded."""
    client = mock_client(Client, **mock_client_kwargs)

    async def _consume() -> list[Any]:
        return [item async for item in stream_endpoint(client=client)]

    return asyncio.run(_consume())


def with_generated_client_fixture(
    openapi_spec: str,
    name: str="generated_client",
    config: str="",
    extra_args: list[str] = [],
):
    """Decorator to apply to a test class to create a fixture inside it called 'generated_client'.

    The fixture value will be a GeneratedClientContext created by calling
    generate_client_from_inline_spec().
    """
    def _decorator(cls):
        def generated_client(self):
            with generate_client_from_inline_spec(openapi_spec, extra_args=extra_args, config=config) as g:
                print(g.generator_result.stdout)  # so we'll see the output if a test failed
                yield g

        setattr(cls, name, pytest.fixture(scope="class")(generated_client))
        return cls

    return _decorator


def with_generated_code_import(import_path: str, alias: str | None = None):
    """Decorator to apply to a test class to create a fixture from a generated code import.

    The 'generated_client' fixture must also be present.

    If import_path is "a.b.c", then the fixture's value is equal to "from a.b import c", and
    its name is "c" unless you specify a different name with the alias parameter.
    """
    parts = import_path.split(".")
    module_name = ".".join(parts[0:-1])
    import_name = parts[-1]

    def _decorator(cls):
        nonlocal alias

        def _func(self, generated_client):
            return generated_client.import_symbol(module_name, import_name)

        alias = alias or import_name
        _func.__name__ = alias
        setattr(cls, alias, pytest.fixture(scope="class")(_func))
        return cls

    return _decorator


def with_generated_code_imports(*import_paths: str):
    def _decorator(cls):
        decorated = cls
        for import_path in import_paths:
            decorated = with_generated_code_import(import_path)(decorated)
        return decorated

    return _decorator


def dump_for_transport(instance: Any) -> Dict[str, Any]:
    """Serialize a generated model the way its own client does.

    Generated models have no public ``to_dict``: serialization lives in
    ``<package>.types.dump_dict__for_transport`` so that there is a single audited
    model-to-wire conversion. Reaching for it here keeps these assertions on the real
    encode path rather than a copy of its arguments that could drift.
    """
    package = type(instance).__module__.rsplit(".models.", 1)[0]
    return importlib.import_module(f"{package}.types").dump_dict__for_transport(instance)


def assert_model_decode_encode(model_class: Any, json_data: dict, expected_instance: Any) -> None:
    instance = model_class.from_dict(json_data)
    assert instance == expected_instance
    assert dump_for_transport(instance) == json_data


def assert_model_property_type_hint(model_class: Any, name: str, expected_type_hint: Any) -> None:
    assert model_class.__annotations__[name] == expected_type_hint


def inline_spec_should_fail(
    openapi_spec: str,
    extra_args: list[str] = [],
    config: str = "",
    filename_suffix: str = "",
    add_missing_sections = True,
) -> Result:
    """Asserts that the generator could not process the spec.

    Returns the command result, which could include stdout data or an exception.
    """
    with generate_client_from_inline_spec(
        openapi_spec,
        extra_args,
        config,
        filename_suffix=filename_suffix,
        add_missing_sections=add_missing_sections,
        raise_on_error=False,
    ) as generated_client:
        assert generated_client.generator_result.exit_code != 0
        return generated_client.generator_result


def assert_bad_schema(
    generated_client: GeneratedClientContext,
    schema_name: str,
    expected_message_str: str,
) -> None:
    warnings = _GeneratorWarningsParser(generated_client)
    assert schema_name in warnings.by_schema, f"Did not find warning for schema {schema_name} in output: {warnings.output}"
    assert expected_message_str in warnings.by_schema[schema_name]


class _GeneratorWarningsParser:
    output: str
    by_schema: Dict[str, str]

    def __init__(self, generated_client: GeneratedClientContext) -> None:
        """Runs the generator, asserts that it printed warnings, and parses the warnings."""

        assert generated_client.generator_result.exit_code == 0
        output = generated_client.generator_result.stdout + generated_client.generator_result.stderr
        assert "Warning(s) encountered while generating" in output
        self.by_schema = {}
        self.output = output
        bad_schema_regex = "Unable to (parse|process) schema /components/schemas/(\\w*)"
        last_name = ""
        while True:
            if not (match := re.search(bad_schema_regex, output)):
                break
            if last_name:
                self.by_schema[last_name] = output[0:match.start()]
            output = output[match.end():]
            last_name = match.group(2)
        if last_name:
            self.by_schema[last_name] = output
