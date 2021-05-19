import shutil
from filecmp import dircmp
from pathlib import Path
from typing import Dict, List, Optional

import pytest
from typer.testing import CliRunner

from openapi_python_client.cli import app


def _dircmp_recursive(dc: dircmp, *, base_path: Path, dc_info: Dict[str, List[Path]]) -> None:
    for k, v in dc_info.items():
        v.extend([base_path / f for f in getattr(dc, k)])

    for sub_dir, sub_dc in dc.subdirs.items():
        _dircmp_recursive(sub_dc, base_path=(base_path / sub_dir), dc_info=dc_info)


def _compare_directories(
    record: Path,
    test_subject: Path,
    expected_differences: Optional[Dict[Path, str]] = None,
):
    first_printable = record.relative_to(Path.cwd())
    second_printable = test_subject.relative_to(Path.cwd())
    dc = dircmp(record, test_subject)
    dc_info = {
        "left_only": [],
        "right_only": [],
        "diff_files": [],
        "common_funny": [],
    }
    _dircmp_recursive(dc, base_path=Path(""), dc_info=dc_info)
    missing_files = dc_info["left_only"] + dc_info["right_only"]
    if missing_files:
        pytest.fail(
            f"{first_printable} or {second_printable} was missing: {list(map(str, missing_files))}",
            pytrace=False,
        )

    expected_differences = expected_differences or {}
    mismatch = set(dc_info["diff_files"])

    for file_name in mismatch | set(expected_differences.keys()):
        if file_name not in expected_differences:
            continue
        if file_name not in mismatch:
            pytest.fail(f"Expected {file_name} to be different but it was not", pytrace=False)
        generated = (test_subject / file_name).read_text()
        assert generated == expected_differences[file_name], f"Unexpected output in {file_name}"
        del expected_differences[file_name]
        mismatch.remove(file_name)

    if mismatch:
        errors = list(map(str, dc_info["common_funny"]))
        mismatch_printable = list(map(str, mismatch))
        pytest.fail(
            f"{first_printable} and {second_printable} had differing files: {mismatch_printable}, and errors {errors}",
            pytrace=False,
        )


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
    expected_differences = {
        "README.md": "my-test-api-client",
        "my_test_api_client/__init__.py": (
            '""" Overriden comment """\nfrom .client import AuthenticatedClient, Client\n'
        ),
        "my_test_api_client/api/__init__.py": '"""Custom comment"""\n',
    }
    run_e2e_test(
        extra_args=["--custom-template-path=end_to_end_tests/test_custom_templates"],
        expected_differences={Path(k): v for k, v in expected_differences.items()},
    )
