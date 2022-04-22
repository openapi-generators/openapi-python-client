from pathlib import Path

import pytest
from jinja2 import Template


@pytest.fixture(scope="session")
def template(env) -> Template:
    return env.get_template("endpoint_module.pyi")


def test_async_module(template, mocker):
    path_param = mocker.MagicMock(python_name="path_param_1")
    path_param.name = "pathParam1"
    path_param.to_string.return_value = "path_param_1: str"
    query_param = mocker.MagicMock(template=None, python_name="query_param_1")
    query_param.name = "queryParam"
    query_param.to_string.return_value = "query_param_1: str"
    header_param = mocker.MagicMock(template=None, python_name="header_param_1")
    header_param.name = "headerParam"
    header_param.to_string.return_value = "header_param_1: str"

    yaml_body = mocker.MagicMock(template=None, python_name="yaml_body")
    yaml_body.get_type_string.return_value = "Json"
    form_body_reference = mocker.MagicMock(class_name="FormBody")
    multipart_body_reference = mocker.MagicMock(class_name="MultiPartBody")
    json_body = mocker.MagicMock(template=None, python_name="json_body")
    json_body.get_type_string.return_value = "Json"
    post_response_1 = mocker.MagicMock(
        status_code=200, source="response.json()", prop=mocker.MagicMock(template=None, python_name="response_one")
    )
    post_response_1.prop.get_type_string.return_value = "str"
    post_response_2 = mocker.MagicMock(
        status_code=201, source="response.json()", prop=mocker.MagicMock(template=None, python_name="response_one")
    )
    post_response_2.prop.get_type_string.return_value = "int"
    post_endpoint = mocker.MagicMock(
        name="camelCase",
        requires_security=True,
        path_parameters=[],
        query_parameters=[],
        yaml_body=yaml_body,
        form_body_reference=form_body_reference,
        multipart_body_reference=multipart_body_reference,
        json_body=json_body,
        responses=[post_response_1, post_response_2],
        description="POST endpoint",
        path="/post/",
        method="post",
        relative_imports=["import this", "from __future__ import braces"],
    )
    post_endpoint.name = "camelCase"

    result = template.render(endpoint=post_endpoint)

    import black

    expected = (Path(__file__).parent / "endpoint_module.py").read_text()
    black.assert_equivalent(result, expected)
