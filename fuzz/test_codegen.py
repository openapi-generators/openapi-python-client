import ast
import io
import json
import os
import subprocess
import tomllib
import warnings
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from hypothesis import given, settings
from hypothesis import strategies as st

from openapi_python_client import Config, ErrorLevel, MetaType, generate
from openapi_python_client.config import ConfigFile
from openapi_python_client.schema import OpenAPI

FUZZ_EXAMPLES = int(os.environ.get("OPENAPI_PYTHON_CLIENT_FUZZ_EXAMPLES", "100"))

# Canary payload: if any untrusted string breaks out of its literal/docstring in generated code,
# this appears as a real AST Name/Call node instead of text inside a string constant.
CANARY = "PWNED_CANARY"
CALL_CANARY = "EXECUTED_CANARY"

DANGEROUS_STRINGS = (
    "",
    "'",
    '"',
    "\\",
    "\n",
    "\r\n",
    "\t",
    "\x00",
    '"""',
    "'''",
    "{value!r}",
    "${value}",
    "{{ value }}",
    "line one\\\nline two",
    "\\U0000000",
    "\\N{NOT A REAL NAME}",
    "# type: ignore\n" + CANARY + "()",
    "\n# comment with trailing slash\\",
    "from os import system",
    "\N{LINE SEPARATOR}",
    "\N{PILE OF POO}",
    f'"{CANARY}("',
    f'"{CANARY}() + "',
    f"'''{CANARY}()'''",
    f'"""{CANARY}()"""',
    f'\\"{CANARY}()',
    f"\n{CANARY}()\n",
    f'"; print("{CALL_CANARY}"); _fuzz = "',
    f'"""\nprint("{CALL_CANARY}")\n"""',
)
UTF8_CHARACTERS = st.characters(blacklist_categories=["Cs"])
UNTRUSTED_TEXT = st.one_of(
    st.sampled_from(DANGEROUS_STRINGS),
    st.text(UTF8_CHARACTERS, max_size=60),
)
NONEMPTY_UNTRUSTED_TEXT = st.one_of(
    st.sampled_from(tuple(value for value in DANGEROUS_STRINGS if value)),
    st.text(UTF8_CHARACTERS, min_size=1, max_size=40),
)
COMPONENT_NAME = st.one_of(
    st.sampled_from(tuple(value for value in DANGEROUS_STRINGS if value and "/" not in value and "~" not in value)),
    st.text(UTF8_CHARACTERS, min_size=1, max_size=30).filter(lambda value: "/" not in value and "~" not in value),
)


@st.composite
def schema_strategy(draw: st.DrawFn) -> dict[str, Any]:
    description = draw(UNTRUSTED_TEXT)
    kind = draw(
        st.sampled_from(
            ("string", "integer", "number", "boolean", "array", "object", "reference", "union", "const", "free_form")
        )
    )

    value: Any
    schema: dict[str, Any] = {"description": description}
    if kind == "string":
        value = draw(UNTRUSTED_TEXT)
        schema.update({"type": "string", "default": value, "example": value})
    elif kind == "integer":
        value = draw(st.integers(min_value=-(2**31), max_value=2**31 - 1))
        schema.update({"type": "integer", "default": value, "example": value})
    elif kind == "number":
        value = draw(st.floats(allow_nan=False, allow_infinity=False, width=32))
        schema.update({"type": "number", "default": value, "example": value})
    elif kind == "boolean":
        value = draw(st.booleans())
        schema.update({"type": "boolean", "default": value, "example": value})
    elif kind == "array":
        schema.update(
            {
                "type": "array",
                "items": {"type": "string", "description": draw(UNTRUSTED_TEXT)},
                "example": [draw(UNTRUSTED_TEXT)],
            }
        )
    elif kind == "object":
        schema.update(
            {
                "title": draw(UNTRUSTED_TEXT),
                "type": "object",
                "properties": {"nested": {"type": "string", "description": draw(UNTRUSTED_TEXT)}},
                "additionalProperties": {"type": "string", "description": draw(UNTRUSTED_TEXT)},
                "example": {"nested": draw(UNTRUSTED_TEXT)},
            }
        )
    elif kind == "union":
        schema = {
            "oneOf": [
                {"type": "string", "description": description},
                {"type": "integer", "description": draw(UNTRUSTED_TEXT)},
            ],
            "description": draw(UNTRUSTED_TEXT),
        }
    elif kind == "const":
        schema = {"const": draw(UNTRUSTED_TEXT), "description": description}
    elif kind == "free_form":
        schema = {"type": "object", "additionalProperties": True, "description": description}
    else:
        schema = {"$ref": "#/components/schemas/Choice"}
    return schema


@st.composite
def openapi_documents(draw: st.DrawFn) -> dict[str, Any]:
    component_name = draw(COMPONENT_NAME)
    property_name = draw(NONEMPTY_UNTRUSTED_TEXT)
    query_name = draw(NONEMPTY_UNTRUSTED_TEXT)
    header_name = draw(NONEMPTY_UNTRUSTED_TEXT)
    cookie_name = draw(NONEMPTY_UNTRUSTED_TEXT)
    path_segment = draw(NONEMPTY_UNTRUSTED_TEXT)
    security_name = draw(NONEMPTY_UNTRUSTED_TEXT)
    property_schema = draw(schema_strategy())
    parameter_schema = draw(schema_strategy())
    enum_values = draw(st.lists(UNTRUSTED_TEXT, min_size=1, max_size=4, unique=True))
    int_enum_values = draw(st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=4, unique=True))

    return {
        "openapi": draw(st.sampled_from(("3.0.0", "3.0.3", "3.1.0"))),
        "info": {
            "title": draw(UNTRUSTED_TEXT),
            "description": draw(UNTRUSTED_TEXT),
            "version": draw(UNTRUSTED_TEXT),
            "termsOfService": draw(UNTRUSTED_TEXT),
            "contact": {
                "name": draw(UNTRUSTED_TEXT),
                "url": draw(UNTRUSTED_TEXT),
                "email": draw(UNTRUSTED_TEXT),
            },
            "license": {"name": draw(NONEMPTY_UNTRUSTED_TEXT), "url": draw(UNTRUSTED_TEXT)},
        },
        "servers": [
            {
                "url": draw(UNTRUSTED_TEXT),
                "description": draw(UNTRUSTED_TEXT),
                "variables": {
                    "fuzz": {
                        "default": draw(UNTRUSTED_TEXT),
                        "enum": [draw(UNTRUSTED_TEXT)],
                        "description": draw(UNTRUSTED_TEXT),
                    }
                },
            }
        ],
        "tags": [{"name": draw(NONEMPTY_UNTRUSTED_TEXT), "description": draw(UNTRUSTED_TEXT)}],
        "externalDocs": {"url": draw(UNTRUSTED_TEXT), "description": draw(UNTRUSTED_TEXT)},
        "security": [{security_name: []}],
        "paths": {
            f"/widgets/{{widget_id}}/{path_segment}": {
                "summary": draw(UNTRUSTED_TEXT),
                "description": draw(UNTRUSTED_TEXT),
                "post": {
                    "operationId": draw(NONEMPTY_UNTRUSTED_TEXT),
                    "tags": [draw(UNTRUSTED_TEXT)],
                    "summary": draw(UNTRUSTED_TEXT),
                    "description": draw(UNTRUSTED_TEXT),
                    "parameters": [
                        {
                            "name": "widget_id",
                            "in": "path",
                            "required": True,
                            "description": draw(UNTRUSTED_TEXT),
                            "schema": {"type": "string"},
                        },
                        {
                            "name": query_name,
                            "in": "query",
                            "description": draw(UNTRUSTED_TEXT),
                            "schema": parameter_schema,
                        },
                        {
                            "name": header_name,
                            "in": "header",
                            "description": draw(UNTRUSTED_TEXT),
                            "schema": {"type": "string", "default": draw(UNTRUSTED_TEXT)},
                        },
                        {
                            "name": cookie_name,
                            "in": "cookie",
                            "description": draw(UNTRUSTED_TEXT),
                            "schema": {"type": "string"},
                        },
                    ],
                    "requestBody": {
                        "required": True,
                        "description": draw(UNTRUSTED_TEXT),
                        "content": {
                            "application/json": {
                                "schema": {"$ref": f"#/components/schemas/{component_name}"},
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": draw(UNTRUSTED_TEXT),
                            "headers": {
                                "X-Fuzz": {
                                    "description": draw(UNTRUSTED_TEXT),
                                    "schema": {"type": "string"},
                                }
                            },
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": f"#/components/schemas/{component_name}"},
                                }
                            },
                        }
                    },
                },
            }
        },
        "components": {
            "securitySchemes": {
                security_name: {
                    "type": "apiKey",
                    "name": draw(NONEMPTY_UNTRUSTED_TEXT),
                    "in": "header",
                    "description": draw(UNTRUSTED_TEXT),
                }
            },
            "schemas": {
                component_name: {
                    "title": draw(UNTRUSTED_TEXT),
                    "type": "object",
                    "description": draw(UNTRUSTED_TEXT),
                    "externalDocs": {"url": draw(UNTRUSTED_TEXT), "description": draw(UNTRUSTED_TEXT)},
                    "xml": {
                        "name": draw(UNTRUSTED_TEXT),
                        "namespace": draw(UNTRUSTED_TEXT),
                        "prefix": draw(UNTRUSTED_TEXT),
                    },
                    "required": [property_name],
                    "properties": {property_name: property_schema},
                },
                "Choice": {
                    "type": "string",
                    "description": draw(UNTRUSTED_TEXT),
                    "enum": enum_values,
                },
                "IntChoice": {
                    "type": "integer",
                    "description": draw(UNTRUSTED_TEXT),
                    "enum": int_enum_values,
                },
            },
        },
    }


@settings(max_examples=FUZZ_EXAMPLES, deadline=None)
@given(document=openapi_documents(), meta_type=st.sampled_from(list(MetaType)))
def test_valid_openapi_never_generates_invalid_python(document: dict[str, Any], meta_type: MetaType) -> None:
    # The generator's own schema model is the source of truth for "valid": anything it accepts
    # must produce syntactically valid Python.
    OpenAPI.model_validate(document)

    with TemporaryDirectory() as temporary_directory:
        root = Path(temporary_directory)
        document_path = root / "openapi.json"
        output_path = root / "generated"
        document_path.write_text(json.dumps(document, ensure_ascii=False), encoding="utf-8")

        config = Config.from_sources(
            ConfigFile(
                project_name_override="fuzz-client",
                package_name_override="fuzz_client",
                post_hooks=[],
            ),
            meta_type,
            document_source=document_path,
            file_encoding="utf-8",
            overwrite=False,
            output_path=output_path,
        )
        with redirect_stdout(io.StringIO()):
            errors = generate(config=config)

        fatal_errors = [error for error in errors if error.level == ErrorLevel.ERROR]
        assert not fatal_errors

        python_files = sorted(output_path.rglob("*.py"))
        assert python_files
        for python_file in python_files:
            source = python_file.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(python_file))
            with warnings.catch_warnings():
                warnings.simplefilter("error")
                compile(source, str(python_file), "exec")
            _assert_no_code_injection(tree, python_file)

        for pyproject_file in output_path.rglob("pyproject.toml"):
            with pyproject_file.open("rb") as pyproject:
                tomllib.load(pyproject)

        # Static analysis catches escapes which produce valid syntax but reference names that
        # don't exist (e.g. an injected function call) — even ones the canary doesn't cover.
        ruff = subprocess.run(
            ["ruff", "check", "--select", "F821", "--no-cache", str(output_path)],
            capture_output=True,
            text=True,
            check=False,
        )
        assert ruff.returncode == 0, f"Generated code references undefined names:\n{ruff.stdout}"


def _assert_no_code_injection(tree: ast.AST, python_file: Path) -> None:
    """Fail if the canary escaped a string literal/docstring and became executable code."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and CANARY in node.id:
            raise AssertionError(f"Canary escaped into a name in {python_file}: {node.id}")
        if isinstance(node, ast.Attribute) and CANARY in node.attr:
            raise AssertionError(f"Canary escaped into an attribute in {python_file}: {node.attr}")
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and CANARY in node.name:
            raise AssertionError(f"Canary escaped into a definition in {python_file}: {node.name}")
        if isinstance(node, ast.ImportFrom) and node.module and CANARY in node.module:
            raise AssertionError(f"Canary escaped into an import in {python_file}: {node.module}")
        if isinstance(node, ast.alias) and CANARY in node.name:
            raise AssertionError(f"Canary escaped into an import in {python_file}: {node.name}")
        if isinstance(node, ast.Call) and any(
            isinstance(child, ast.Constant) and child.value == CALL_CANARY for child in ast.walk(node)
        ):
            raise AssertionError(f"Built-in call canary became executable code in {python_file}")
