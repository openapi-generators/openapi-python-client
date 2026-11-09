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


def test_endpoint_arguments_multi_body_required(env) -> None:
    template = env.get_template("endpoint_macros.py.jinja")
    body1 = SimpleNamespace(
        prop=SimpleNamespace(required=True, get_type_string=lambda no_optional=False: PythonCode("ItemA"))
    )
    body2 = SimpleNamespace(
        prop=SimpleNamespace(required=True, get_type_string=lambda no_optional=False: PythonCode("ItemB"))
    )
    endpoint = SimpleNamespace(
        path_parameters=[],
        query_parameters=[],
        header_parameters=[],
        cookie_parameters=[],
        requires_security=False,
        bodies=[body1, body2],
        list_all_parameters=lambda: [body1.prop, body2.prop],
    )

    result = template.module.arguments(endpoint, include_client=False)
    assert "Unset" not in result
    assert "UNSET" not in result


def test_endpoint_arguments_multi_body_optional(env) -> None:
    template = env.get_template("endpoint_macros.py.jinja")
    body1 = SimpleNamespace(
        prop=SimpleNamespace(required=True, get_type_string=lambda no_optional=False: PythonCode("ItemA"))
    )
    body2 = SimpleNamespace(
        prop=SimpleNamespace(required=False, get_type_string=lambda no_optional=False: PythonCode("ItemB"))
    )
    endpoint = SimpleNamespace(
        path_parameters=[],
        query_parameters=[],
        header_parameters=[],
        cookie_parameters=[],
        requires_security=False,
        bodies=[body1, body2],
        list_all_parameters=lambda: [body1.prop, body2.prop],
    )

    result = template.module.arguments(endpoint, include_client=False)
    assert "| Unset = UNSET" in result
