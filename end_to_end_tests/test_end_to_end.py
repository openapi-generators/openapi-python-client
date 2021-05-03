import shutil
from filecmp import cmpfiles, dircmp
from pathlib import Path
from typing import Dict, Optional

import pytest
from typer.testing import CliRunner

from openapi_python_client.cli import app


def _compare_directories(
    record: Path,
    test_subject: Path,
    expected_differences: Optional[
        Dict[str, str]
    ] = None,  # key: path relative to generated directory, value: expected generated content
    depth=0,
):
    first_printable = record.relative_to(Path.cwd())
    second_printable = test_subject.relative_to(Path.cwd())
    dc = dircmp(record, test_subject)
    missing_files = dc.left_only + dc.right_only
    if missing_files:
        pytest.fail(f"{first_printable} or {second_printable} was missing: {missing_files}", pytrace=False)

    expected_differences = expected_differences or {}
    _, mismatches, errors = cmpfiles(record, test_subject, dc.common_files, shallow=False)
    mismatches = set(mismatches)

    expected_path_mismatches = []
    for file_name in mismatches:

        mismatch_file_path = test_subject.joinpath(file_name)
        for expected_differences_path in expected_differences.keys():

            if mismatch_file_path.match(str(expected_differences_path)):

                generated_content = (test_subject / file_name).read_text()
                expected_content = expected_differences[expected_differences_path]
                assert generated_content == expected_content, f"Unexpected output in {mismatch_file_path}"
                expected_path_mismatches.append(expected_differences_path)

    for path_mismatch in expected_path_mismatches:
        matched_file_name = path_mismatch.name
        mismatches.remove(matched_file_name)
        del expected_differences[path_mismatch]

    if mismatches:
        pytest.fail(
            f"{first_printable} and {second_printable} had differing files: {mismatches}, and errors {errors}",
            pytrace=False,
        )

    for sub_path in dc.common_dirs:
        _compare_directories(
            record / sub_path, test_subject / sub_path, expected_differences=expected_differences, depth=depth + 1
        )

    if depth == 0 and len(expected_differences.keys()) > 0:
        failure = "\n".join([f"Expected {path} to be different but it was not" for path in expected_differences.keys()])
        pytest.fail(failure, pytrace=False)


def run_e2e_test(extra_args=None, expected_differences=None):
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

    _compare_directories(gr_path, output_path, expected_differences=expected_differences)

    import mypy.api

    out, err, status = mypy.api.run([str(output_path), "--strict"])
    assert status == 0, f"Type checking client failed: {out}"

    shutil.rmtree(output_path)


def test_end_to_end():
    run_e2e_test()


def test_custom_templates():
    expected_differences = {}  # key: path relative to generated directory, value: expected generated content
    expected_difference_paths = [
        Path("README.md"),
        Path("my_test_api_client").joinpath("api", "__init__.py"),
        Path("my_test_api_client").joinpath("api", "tests", "__init__.py"),
        Path("my_test_api_client").joinpath("api", "default", "__init__.py"),
        Path("my_test_api_client").joinpath("api", "parameters", "__init__.py"),
    ]

    golden_tpls_root_dir = Path(__file__).parent.joinpath("custom-templates-golden-record")
    for expected_difference_path in expected_difference_paths:
        path = Path("my-test-api-client").joinpath(expected_difference_path)
        expected_differences[path] = (golden_tpls_root_dir / expected_difference_path).read_text()

    run_e2e_test(
        extra_args=["--custom-template-path=end_to_end_tests/test_custom_templates/"],
        expected_differences=expected_differences,
    )
