import shutil
from filecmp import cmpfiles, dircmp
from pathlib import Path

import pytest
from typer.testing import CliRunner

from openapi_python_client.cli import app


def _compare_directories(first: Path, second: Path):
    first_printable = first.relative_to(Path.cwd())
    second_printable = second.relative_to(Path.cwd())
    dc = dircmp(first, second)
    missing_files = dc.left_only + dc.right_only
    if missing_files:
        pytest.fail(f"{first_printable} or {second_printable} was missing: {missing_files}", pytrace=False)

    _, mismatch, errors = cmpfiles(first, second, dc.common_files, shallow=False)
    if mismatch:
        pytest.fail(
            f"{first_printable} and {second_printable} had differing files: {mismatch}, and errors {errors}",
            pytrace=False,
        )

    for sub_path in dc.common_dirs:
        _compare_directories(first / sub_path, second / sub_path)


def test_end_to_end():
    runner = CliRunner()
    openapi_path = Path(__file__).parent / "openapi.json"
    config_path = Path(__file__).parent / "config.yml"
    gr_path = Path(__file__).parent / "golden-record"
    output_path = Path.cwd() / "my-test-api-client"
    shutil.rmtree(output_path, ignore_errors=True)

    result = runner.invoke(app, [f"--config={config_path}", "generate", f"--path={openapi_path}"])

    if result.exit_code != 0:
        raise result.exception
    _compare_directories(gr_path, output_path)

    import mypy.api

    out, err, status = mypy.api.run([str(output_path), "--strict"])
    assert status == 0, f"Type checking client failed: {out}"

    shutil.rmtree(output_path)


def test_end_to_end_w_custom_templates():
    runner = CliRunner()
    openapi_path = Path(__file__).parent / "openapi.json"
    config_path = Path(__file__).parent / "custom_config.yml"
    gr_path = Path(__file__).parent / "golden-record-custom"
    output_path = Path.cwd() / "custom-e2e"
    shutil.rmtree(output_path, ignore_errors=True)

    result = runner.invoke(
        app,
        [
            f"--config={config_path}",
            "generate",
            f"--path={openapi_path}",
            "--custom-template-path=end_to_end_tests/test_custom_templates",
        ],
    )

    if result.exit_code != 0:
        raise result.exception
    _compare_directories(gr_path, output_path)

    shutil.rmtree(output_path)
