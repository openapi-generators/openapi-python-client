import os
import shutil
from filecmp import dircmp, cmpfiles
from pathlib import Path

import pytest
from typer.testing import CliRunner
from openapi_python_client.cli import app


def _compare_directories(first: Path, second: Path, /):
    first_printable = first.relative_to(Path.cwd())
    second_printable = second.relative_to(Path.cwd())
    dc = dircmp(first, second)
    missing_files = dc.left_only + dc.right_only
    if missing_files:
        pytest.fail(f"{first_printable} or {second_printable} was missing: {missing_files}", pytrace=False)

    match, mismatch, errors = cmpfiles(first, second, dc.common_files, shallow=False)
    if mismatch:
        pytest.fail(f"{first_printable} and {second_printable} had differing files: {mismatch}", pytrace=False)

    for sub_path in dc.common_dirs:
        _compare_directories(first / sub_path, second / sub_path)


def test_end_to_end(capsys):
    runner = CliRunner()
    openapi_path = Path(__file__).parent / "fastapi" / "openapi.json"
    gm_path = Path(__file__).parent / "golden-master"
    output_path = Path.cwd() / "my-test-api-client"

    runner.invoke(app, ["generate", f"--path={openapi_path}"])

    _compare_directories(gm_path, output_path)
    shutil.rmtree(output_path)
