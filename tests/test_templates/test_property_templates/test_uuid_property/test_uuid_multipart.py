"""Tests for UUID property multipart macro functionality."""

from pathlib import Path
from typing import Any
from uuid import UUID

import jinja2
import pytest

from openapi_python_client.parser.properties import UuidProperty
from openapi_python_client.utils import PythonIdentifier


def uuid_property(required: bool = True, default: Any = None) -> UuidProperty:
    """Helper to create a UuidProperty for testing."""
    return UuidProperty(
        name="test_uuid",
        required=required,
        default=default,
        python_name=PythonIdentifier(value="test_uuid", prefix=""),
        description="A test UUID property",
        example="550e8400-e29b-41d4-a716-446655440000",
    )


@pytest.fixture
def jinja_env() -> jinja2.Environment:
    """Create a Jinja2 environment with the property templates loaded."""
    templates_dir = Path(__file__).parent.parent.parent.parent.parent / "openapi_python_client" / "templates"
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(templates_dir),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    return env


def test_multipart_macro_generates_syntactically_correct_code_for_required_uuid(jinja_env: jinja2.Environment) -> None:
    """Test that the multipart macro generates syntactically correct Python code for required UUID properties."""
    prop = uuid_property(required=True)

    template = jinja_env.get_template("property_templates/uuid_property.py.jinja")

    # Render the multipart macro
    multipart_code = template.module.multipart(prop, "test_uuid", '"test_uuid"')  # type: ignore[attr-defined]

    # Verify the generated code is syntactically correct
    expected = 'files.append(("test_uuid", (None, str(test_uuid), "text/plain")))'
    assert multipart_code.strip() == expected

    # Verify it compiles as valid Python
    compile(multipart_code, "<string>", "exec")


def test_multipart_macro_generates_syntactically_correct_code_for_optional_uuid(jinja_env: jinja2.Environment) -> None:
    """Test that the multipart macro generates syntactically correct Python code for optional UUID properties."""
    prop = uuid_property(required=False)

    template = jinja_env.get_template("property_templates/uuid_property.py.jinja")

    # Render the multipart macro
    multipart_code = template.module.multipart(prop, "test_uuid", '"test_uuid"')  # type: ignore[attr-defined]

    # Verify the generated code is syntactically correct
    expected = 'files.append(("test_uuid", (None, str(test_uuid), "text/plain")))'
    assert multipart_code.strip() == expected

    # Verify it compiles as valid Python
    compile(multipart_code, "<string>", "exec")
    