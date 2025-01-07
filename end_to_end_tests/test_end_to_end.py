import shutil
from filecmp import cmpfiles, dircmp
from pathlib import Path
from typing import Optional

import pytest
from click.testing import Result
from typer.testing import CliRunner

from openapi_python_client.cli import app


def _compare_directories(
    record: Path,
    test_subject: Path,
    expected_differences: Optional[dict[Path, str]] = None,
    expected_missing: Optional[set[str]] = None,
    ignore: list[str] = None,
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
    dc = dircmp(record, test_subject, ignore=[".ruff_cache", "__pycache__"] + (ignore or []))
    missing_files = set(dc.left_only + dc.right_only) - (expected_missing or set())
    if missing_files:
        pytest.fail(
            f"{first_printable} or {second_printable} was missing: {missing_files}",
            pytrace=False,
        )

    expected_differences = expected_differences or {}
    _, mismatches, errors = cmpfiles(
        record, test_subject, dc.common_files, shallow=False
    )
    mismatches = set(mismatches)

    for file_name in mismatches:
        mismatch_file_path = test_subject.joinpath(file_name)

        if mismatch_file_path in expected_differences:
            expected_content = expected_differences[mismatch_file_path]
            del expected_differences[mismatch_file_path]
        else:
            expected_content = (record / file_name).read_text()

        generated_content = (test_subject / file_name).read_text()
        assert (
            generated_content == expected_content
        ), f"Unexpected output in {mismatch_file_path}"

    for sub_path in dc.common_dirs:
        _compare_directories(
            record / sub_path,
            test_subject / sub_path,
            expected_differences=expected_differences,
            ignore=ignore,
            depth=depth + 1,
        )

    if depth == 0 and len(expected_differences.keys()) > 0:
        failure = "\n".join(
            [
                f"Expected {path} to be different but it was not"
                for path in expected_differences.keys()
            ]
        )
        pytest.fail(failure, pytrace=False)


def run_e2e_test(
    openapi_document: str,
    extra_args: list[str],
    expected_differences: Optional[dict[Path, str]] = None,
    golden_record_path: str = "golden-record",
    output_path: str = "my-test-api-client",
    expected_missing: Optional[set[str]] = None,
) -> Result:
    output_path = Path.cwd() / output_path
    shutil.rmtree(output_path, ignore_errors=True)
    result = generate(extra_args, openapi_document)
    gr_path = Path(__file__).parent / golden_record_path

    expected_differences = expected_differences or {}
    # Use absolute paths for expected differences for easier comparisons
    expected_differences = {
        output_path.joinpath(key): value for key, value in expected_differences.items()
    }
    _compare_directories(
        gr_path, output_path, expected_differences=expected_differences, expected_missing=expected_missing
    )

    import mypy.api

    out, err, status = mypy.api.run([str(output_path), "--strict"])
    assert status == 0, f"Type checking client failed: {out}"

    shutil.rmtree(output_path)
    return result


def generate(extra_args: Optional[list[str]], openapi_document: str) -> Result:
    """Generate a client from an OpenAPI document and return the path to the generated code"""
    _run_command("generate", extra_args, openapi_document)


def _run_command(command: str, extra_args: Optional[list[str]] = None, openapi_document: Optional[str] = None, url: Optional[str] = None, config_path: Optional[Path] = None) -> Result:
    """Generate a client from an OpenAPI document and return the path to the generated code"""
    runner = CliRunner()
    if openapi_document is not None:
        openapi_path = Path(__file__).parent / openapi_document
        source_arg = f"--path={openapi_path}"
    else:
        source_arg = f"--url={url}"
    config_path = config_path or (Path(__file__).parent / "config.yml")
    args = [command, f"--config={config_path}", source_arg]
    if extra_args:
        args.extend(extra_args)
    result = runner.invoke(app, args)
    if result.exit_code != 0:
        raise Exception(result.stdout)
    return result


def test_baseline_end_to_end_3_0():
    run_e2e_test("baseline_openapi_3.0.json", [], {})


def test_baseline_end_to_end_3_1():
    run_e2e_test("baseline_openapi_3.1.yaml", [], {})


def test_3_1_specific_features():
    run_e2e_test(
        "3.1_specific.openapi.yaml",
        [],
        {},
        "test-3-1-golden-record",
        "test-3-1-features-client",
    )


def test_literal_enums_end_to_end():
    config_path = Path(__file__).parent / "literal_enums.config.yml"
    run_e2e_test(
        "openapi_3.1_enums.yaml",
        [f"--config={config_path}"],
        {},
        "literal-enums-golden-record",
        "my-enum-api-client"
    )


@pytest.mark.parametrize(
    "meta,generated_file,expected_file",
    (
        ("setup", "setup.py", "setup.py"),
        ("pdm", "pyproject.toml", "pdm.pyproject.toml"),
        ("poetry", "pyproject.toml", "poetry.pyproject.toml"),
    )
)
def test_meta(meta: str, generated_file: Optional[str], expected_file: Optional[str]):
    output_path = Path.cwd() / "test-3-1-features-client"
    shutil.rmtree(output_path, ignore_errors=True)
    generate([f"--meta={meta}"], "3.1_specific.openapi.yaml")

    if generated_file and expected_file:
        assert (output_path / generated_file).exists()
        assert (
            (output_path / generated_file).read_text() ==
            (Path(__file__).parent / "metadata_snapshots" / expected_file).read_text()
        )

    shutil.rmtree(output_path)


def test_none_meta():
    run_e2e_test(
        "3.1_specific.openapi.yaml",
        ["--meta=none"],
        golden_record_path="test-3-1-golden-record/test_3_1_features_client",
        output_path="test_3_1_features_client",
        expected_missing={"py.typed"},
    )


def test_docstrings_on_attributes():
    config_path = Path(__file__).parent / "docstrings_on_attributes.config.yml"
    run_e2e_test(
        "docstrings_on_attributes.yml",
        [f"--config={config_path}"],
        {},
        "docstrings-on-attributes-golden-record",
    )


def test_custom_templates():
    expected_differences = (
        {}
    )  # key: path relative to generated directory, value: expected generated content
    api_dir = Path("my_test_api_client").joinpath("api")
    golden_tpls_root_dir = Path(__file__).parent.joinpath(
        "custom-templates-golden-record"
    )

    expected_difference_paths = [
        Path("README.md"),
        api_dir.joinpath("__init__.py"),
    ]

    for expected_difference_path in expected_difference_paths:
        expected_differences[expected_difference_path] = (
            golden_tpls_root_dir / expected_difference_path
        ).read_text()

    # Each API module (defined by tag) has a custom __init__.py in it now.
    for endpoint_mod in golden_tpls_root_dir.joinpath(api_dir).iterdir():
        if not endpoint_mod.is_dir():
            continue
        relative_path = api_dir.joinpath(endpoint_mod.name, "__init__.py")
        expected_text = endpoint_mod.joinpath("__init__.py").read_text()
        expected_differences[relative_path] = expected_text

    run_e2e_test(
        "baseline_openapi_3.0.json",
        extra_args=["--custom-template-path=end_to_end_tests/test_custom_templates/"],
        expected_differences=expected_differences,
    )


def test_bad_url():
    runner = CliRunner()
    result = runner.invoke(app, ["generate", "--url=not_a_url"])
    assert result.exit_code == 1
    assert "Could not get OpenAPI document from provided URL" in result.stdout


ERROR_DOCUMENTS = [path for path in Path(__file__).parent.joinpath("documents_with_errors").iterdir() if path.is_file()]


@pytest.mark.parametrize("document", ERROR_DOCUMENTS, ids=[path.stem for path in ERROR_DOCUMENTS])
def test_documents_with_errors(snapshot, document):
    runner = CliRunner()
    output_path = Path.cwd() / "test-documents-with-errors"
    shutil.rmtree(output_path, ignore_errors=True)
    result = runner.invoke(app, ["generate", f"--path={document}", "--fail-on-warning", f"--output-path={output_path}"])
    assert result.exit_code == 1
    assert result.stdout.replace(str(output_path), "/test-documents-with-errors") == snapshot
    shutil.rmtree(output_path, ignore_errors=True)


def test_custom_post_hooks():
    shutil.rmtree(Path.cwd() / "my-test-api-client", ignore_errors=True)
    runner = CliRunner()
    openapi_document = Path(__file__).parent / "baseline_openapi_3.0.json"
    config_path = Path(__file__).parent / "custom_post_hooks.config.yml"
    result = runner.invoke(app, ["generate", f"--path={openapi_document}", f"--config={config_path}"])
    assert result.exit_code == 1
    assert "this should fail" in result.stdout
    shutil.rmtree(Path.cwd() / "my-test-api-client", ignore_errors=True)


def test_generate_dir_already_exists():
    project_dir = Path.cwd() / "my-test-api-client"
    if not project_dir.exists():
        project_dir.mkdir()
    runner = CliRunner()
    openapi_document = Path(__file__).parent / "baseline_openapi_3.0.json"
    result = runner.invoke(app, ["generate", f"--path={openapi_document}"])
    assert result.exit_code == 1
    assert "Directory already exists" in result.stdout
    shutil.rmtree(Path.cwd() / "my-test-api-client", ignore_errors=True)


@pytest.mark.parametrize(
    ("file_name", "content", "expected_error"),
    (
        ("invalid_openapi.yaml", "not a valid openapi document", "Failed to parse OpenAPI document"),
        ("invalid_json.json", "Invalid JSON", "Invalid JSON"),
        ("invalid_yaml.yaml", "{", "Invalid YAML"),
    ),
    ids=("invalid_openapi", "invalid_json", "invalid_yaml")
)
def test_invalid_openapi_document(file_name, content, expected_error):
    runner = CliRunner()
    openapi_document = Path.cwd() / file_name
    openapi_document.write_text(content)
    result = runner.invoke(app, ["generate", f"--path={openapi_document}"])
    assert result.exit_code == 1
    assert expected_error in result.stdout
    openapi_document.unlink()


def test_update_integration_tests():
    url = "https://raw.githubusercontent.com/openapi-generators/openapi-test-server/main/openapi.json"
    source_path = Path(__file__).parent.parent / "integration-tests"
    temp_dir = Path.cwd() / "test_update_integration_tests"
    shutil.rmtree(temp_dir, ignore_errors=True)
    shutil.copytree(source_path, temp_dir)
    config_path = source_path / "config.yaml"
    _run_command(
        "generate",
        extra_args=["--overwrite", "--meta=pdm", f"--output-path={temp_dir}"],
        url=url,
        config_path=config_path
    )
    _compare_directories(source_path, temp_dir, ignore=["pyproject.toml"])
    import mypy.api

    out, err, status = mypy.api.run([str(temp_dir), "--strict"])
    assert status == 0, f"Type checking client failed: {out}"
    shutil.rmtree(temp_dir)
