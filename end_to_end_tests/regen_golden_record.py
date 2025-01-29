""" Regenerate golden-record """
import filecmp
import shutil
from pathlib import Path
from typing import Optional

from typer.testing import CliRunner

from openapi_python_client.cli import app


def _regenerate(
    *,
    spec_file_name: str,
    output_dir: str = "my-test-api-client",
    golden_record_dir: Optional[str] = None,
    config_file_name: str = "config.yml",
    extra_args: Optional[list[str]] = None
) -> None:
    end_to_end_tests_base_path = Path(__file__).parent
    project_base_path = end_to_end_tests_base_path.parent
    runner = CliRunner()
    openapi_path = end_to_end_tests_base_path / spec_file_name

    output_path = project_base_path / output_dir
    shutil.rmtree(output_path, ignore_errors=True)

    args = ["generate", f"--path={openapi_path}"]
    if config_file_name:
        config_path = end_to_end_tests_base_path / config_file_name
        args.append(f"--config={config_path}")
    if extra_args:
        args.extend(extra_args)
    print(f"Using {spec_file_name}{f' and {config_file_name}' if config_file_name else ''}")

    result = runner.invoke(app, args)

    if result.stdout:
        print(result.stdout)
    if result.exception:
        raise result.exception
    if golden_record_dir:
        gr_path = end_to_end_tests_base_path / golden_record_dir
        shutil.rmtree(gr_path, ignore_errors=True)
        output_path.rename(gr_path)


def regen_golden_record():
    _regenerate(
        spec_file_name="baseline_openapi_3.0.json",
        golden_record_dir="golden-record",
    )


def regen_golden_record_3_1_features():
    _regenerate(
        spec_file_name="3.1_specific.openapi.yaml",
        output_dir="test-3-1-features-client",
        golden_record_dir="test-3-1-golden-record",
    )


def regen_literal_enums_golden_record():
    _regenerate(
        spec_file_name="openapi_3.1_enums.yaml",
        output_dir="my-enum-api-client",
        golden_record_dir="literal-enums-golden-record",
        config_file_name="literal_enums.config.yml",
    )


def regen_metadata_snapshots():
    output_path = Path.cwd() / "test-3-1-features-client"
    snapshots_dir = Path(__file__).parent / "metadata_snapshots"

    for (meta, file, rename_to) in (("setup", "setup.py", "setup.py"), ("pdm", "pyproject.toml", "pdm.pyproject.toml"), ("poetry", "pyproject.toml", "poetry.pyproject.toml")):
        _regenerate(
            spec_file_name="3.1_specific.openapi.yaml",
            output_dir="test-3-1-features-client",
            extra_args=[f"--meta={meta}"],
        )
        (output_path / file).rename(snapshots_dir / rename_to)

    shutil.rmtree(output_path, ignore_errors=True)


def regen_docstrings_on_attributes_golden_record():
    _regenerate(
        spec_file_name="docstrings_on_attributes.yml",
        golden_record_dir="docstrings-on-attributes-golden-record",
        config_file_name="docstrings_on_attributes.config.yml",
    )


def regen_custom_template_golden_record():
    runner = CliRunner()
    openapi_path = Path(__file__).parent / "baseline_openapi_3.0.json"
    tpl_dir = Path(__file__).parent / "test_custom_templates"

    gr_path = Path(__file__).parent / "golden-record"
    tpl_gr_path = Path(__file__).parent / "custom-templates-golden-record"

    output_path = Path.cwd() / "my-test-api-client"
    config_path = Path(__file__).parent / "config.yml"

    shutil.rmtree(tpl_gr_path, ignore_errors=True)

    result = runner.invoke(
        app,
        [
            "generate",
            f"--config={config_path}",
            f"--path={openapi_path}",
            f"--custom-template-path={tpl_dir}",
        ],
    )

    if result.stdout:
        for f in output_path.glob("**/*"):  # nb: works for Windows and Unix
            relative_to_generated = f.relative_to(output_path)
            gr_file = gr_path / relative_to_generated
            if not gr_file.exists():
                print(f"{gr_file} does not exist, ignoring")
                continue

            if not gr_file.is_file():
                continue

            if not filecmp.cmp(gr_file, f, shallow=False):
                target_file = tpl_gr_path / relative_to_generated
                target_dir = target_file.parent

                target_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy(f"{f}", f"{target_file}")

        shutil.rmtree(output_path, ignore_errors=True)

    if result.exception:
        shutil.rmtree(output_path, ignore_errors=True)
        raise result.exception


if __name__ == "__main__":
    regen_golden_record()
    regen_golden_record_3_1_features()
    regen_metadata_snapshots()
    regen_docstrings_on_attributes_golden_record()
    regen_custom_template_golden_record()
    regen_literal_enums_golden_record()
