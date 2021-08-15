import os
import shutil
from filecmp import cmpfiles, dircmp
from pathlib import Path
from typing import Dict, List, Optional

import pytest
from typer.testing import CliRunner

from openapi_python_client.cli import app


def _compare_directories(
    record: Path,
    test_subject: Path,
    expected_differences: Dict[Path, str],
    depth=0,
):
    """
    Compare two directories and assert that only expected_differences are different

    Args:
        record: Path to the expected output
        test_subject: Path to the generated code being checked
        expected_differences: key: path relative to generated directory, value: expected generated content
        depth: Used to track recursion
    """
    first_printable = record.relative_to(Path.cwd())
    second_printable = test_subject.relative_to(Path.cwd())
    dc = dircmp(record, test_subject)
    missing_files = dc.left_only + dc.right_only
    if missing_files:
        pytest.fail(f"{first_printable} or {second_printable} was missing: {missing_files}", pytrace=False)

    expected_differences = expected_differences or {}
    _, mismatches, errors = cmpfiles(record, test_subject, dc.common_files, shallow=False)
    mismatches = set(mismatches)

    for file_name in mismatches:
        mismatch_file_path = test_subject.joinpath(file_name)

        if mismatch_file_path in expected_differences:
            expected_content = expected_differences[mismatch_file_path]
            del expected_differences[mismatch_file_path]
        else:
            expected_content = (record / file_name).read_text()

        generated_content = (test_subject / file_name).read_text()
        assert generated_content == expected_content, f"Unexpected output in {mismatch_file_path}"

    for sub_path in dc.common_dirs:
        _compare_directories(
            record / sub_path, test_subject / sub_path, expected_differences=expected_differences, depth=depth + 1
        )

    if depth == 0 and len(expected_differences.keys()) > 0:
        failure = "\n".join([f"Expected {path} to be different but it was not" for path in expected_differences.keys()])
        pytest.fail(failure, pytrace=False)


def run_e2e_test(extra_args: List[str], expected_differences: Dict[Path, str]):
    runner = CliRunner()
    openapi_path = Path(__file__).parent / "openapi.json"
    config_path = Path(__file__).parent / "config.yml"
    gr_path = Path(__file__).parent / "golden-record"
    output_path = Path.cwd() / "my-test-api-client"
    shutil.rmtree(output_path, ignore_errors=True)

    args = ["generate", f"--config={config_path}", f"--path={openapi_path}"]
    if extra_args:
        args.extend(extra_args)
    result = runner.invoke(app, args)

    if result.exit_code != 0:
        raise result.exception

    # Use absolute paths for expected differences for easier comparisons
    expected_differences = {output_path.joinpath(key): value for key, value in expected_differences.items()}
    _compare_directories(gr_path, output_path, expected_differences=expected_differences)

    import mypy.api

    out, err, status = mypy.api.run([str(output_path), "--strict"])
    assert status == 0, f"Type checking client failed: {out}"

    shutil.rmtree(output_path)


def test_end_to_end():
    run_e2e_test([], {})


def test_custom_templates():
    expected_differences = {}  # key: path relative to generated directory, value: expected generated content
    api_dir = Path("my_test_api_client").joinpath("api")
    golden_tpls_root_dir = Path(__file__).parent.joinpath("custom-templates-golden-record")

    expected_difference_paths = [
        Path("README.md"),
        api_dir.joinpath("__init__.py"),
    ]

    for expected_difference_path in expected_difference_paths:
        expected_differences[expected_difference_path] = (golden_tpls_root_dir / expected_difference_path).read_text()

    # Each API module (defined by tag) has a custom __init__.py in it now.
    for endpoint_mod in golden_tpls_root_dir.joinpath(api_dir).iterdir():
        if not endpoint_mod.is_dir():
            continue
        relative_path = api_dir.joinpath(endpoint_mod.name, "__init__.py")
        expected_text = endpoint_mod.joinpath("__init__.py").read_text()
        expected_differences[relative_path] = expected_text

    run_e2e_test(
        extra_args=["--custom-template-path=end_to_end_tests/test_custom_templates/"],
        expected_differences=expected_differences,
    )
