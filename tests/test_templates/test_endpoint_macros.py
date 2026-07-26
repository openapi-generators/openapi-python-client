from types import SimpleNamespace

from openapi_python_client.strings import PythonCode


def _render_docstring(env, return_string, is_detailed: bool) -> str:
    template = env.get_template("endpoint_macros.py.jinja")
    endpoint = SimpleNamespace(summary=None, description=None, list_all_parameters=lambda: [])
    return template.module.docstring(endpoint, return_string, is_detailed)


def test_endpoint_docstring_escapes_return_string(env) -> None:
    """The return type is rendered inside endpoint docstrings; it must not be able to break out.

    Type strings can embed literal values (e.g. const `Literal[...]`), so the docstring macro must pass the
    return string through `safe_for_docstring` rather than rendering the raw code. Note that a raw breakout
    would still be *valid* Python (that's the point of an escape), so this asserts on the docstring content,
    not just parseability.
    """
    nasty = 'Literal[\'""" + print("uh oh") + """\']'

    for is_detailed in (True, False):
        result = _render_docstring(env, nasty, is_detailed)
        # Only the two docstring delimiters; the value's triple-quotes must be escaped
        assert result.count('"""') == 2
        assert '\\"\\"\\"' in result


def test_endpoint_docstring_unwraps_python_code_return_string(env) -> None:
    """A PythonCode return type must render its (escaped) code in the docstring, not the safe pointer repr"""
    code = PythonCode("MyModel | None")

    result = _render_docstring(env, code, is_detailed=False)

    assert "MyModel | None" in result
    assert "object at 0x" not in result
