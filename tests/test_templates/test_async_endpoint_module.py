from pathlib import Path

import pytest
from jinja2 import Template


@pytest.fixture(scope="session")
def template(env) -> Template:
    return env.get_template("async_endpoint_module.pyi")


def test_async_endpoint_module(template, mocker):
    path_param = mocker.MagicMock(python_name="path_param_1")
    path_param.name = "pathParam1"
    path_param.to_string.return_value = "path_param_1: str"
    query_param = mocker.MagicMock(template=None, python_name="query_param_1")
    query_param.name = "queryParam"
    query_param.to_string.return_value = "query_param_1: str"
    header_param = mocker.MagicMock(template=None, python_name="header_param_1")
    header_param.name = "headerParam"
    header_param.to_string.return_value = "header_param_1: str"
    get_response = mocker.MagicMock(status_code=200)
    get_response.return_string.return_value = "str"
    get_response.constructor.return_value = "str(response.text)"
    get_endpoint = mocker.MagicMock(
        requires_security=False,
        path_parameters=[path_param],
        query_parameters=[query_param],
        header_parameters=[header_param],
        form_body_reference=None,
        multipart_body_reference=None,
        json_body=None,
        responses=[get_response],
        description="GET endpoint",
        path="/get/{pathParam1}",
        method="get",
    )
    get_endpoint.name = "PascalCase"

    form_body_reference = mocker.MagicMock(class_name="FormBody")
    multipart_body_reference = mocker.MagicMock(class_name="MultiPartBody")
    json_body = mocker.MagicMock(template=None, python_name="json_body")
    json_body.get_type_string.return_value = "Json"
    post_response_1 = mocker.MagicMock(status_code=200)
    post_response_1.return_string.return_value = "str"
    post_response_1.constructor.return_value = "str(response.text)"
    post_response_2 = mocker.MagicMock(status_code=201)
    post_response_2.return_string.return_value = "int"
    post_response_2.constructor.return_value = "int(response.text)"
    post_endpoint = mocker.MagicMock(
        name="camelCase",
        requires_security=True,
        path_parameters=[],
        query_parameters=[],
        form_body_reference=form_body_reference,
        multipart_body_reference=multipart_body_reference,
        json_body=json_body,
        responses=[post_response_1, post_response_2],
        description="POST endpoint",
        path="/post/",
        method="post",
    )
    post_endpoint.name = "camelCase"

    collection = mocker.MagicMock(
        relative_imports=["import this", "from __future__ import braces"], endpoints=[get_endpoint, post_endpoint],
    )

    result = template.render(collection=collection)
    import black
    expected = (Path(__file__).parent / "async_endpoint_module.py").read_text()
    black.assert_equivalent(result, expected)
