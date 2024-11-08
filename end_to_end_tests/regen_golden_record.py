""" Regenerate golden-record """
import filecmp
import os
import shutil
import tempfile
from pathlib import Path

from typer.testing import CliRunner

from openapi_python_client.cli import app


def regen(
    spec_file_name: str,
    config_file_name: str,
    golden_record_dir_name: str,
    output_dir_name: str,
):
    runner = CliRunner()
    openapi_path = Path(__file__).parent / spec_file_name

    gr_path = Path(__file__).parent / golden_record_dir_name
    output_path = Path.cwd() / output_dir_name
    config_path = Path(__file__).parent / config_file_name if config_file_name else None

    shutil.rmtree(gr_path, ignore_errors=True)
    shutil.rmtree(output_path, ignore_errors=True)

    args = [
        "generate",
        f"--path={openapi_path}",
        *([f"--config={config_path}"] if config_path else []),
    ]
    result = runner.invoke(app, args)

    if result.stdout:
        print(result.stdout)
    if result.exception:
        raise result.exception
    output_path.rename(gr_path)


def regen_golden_record():
    regen("baseline_openapi_3.0.json", "config.yml", "golden-record", "my-test-api-client")


def regen_golden_record_3_1_features():
    regen("3.1_specific.openapi.yaml", "", "test-3-1-golden-record", "test-3-1-features-client")


def regen_literal_enums_golden_record():
    regen("openapi_3.1_enums.yaml", "literal_enums.config.yml", "literal-enums-golden-record", "my-enum-api-client")


def regen_metadata_snapshots():
    runner = CliRunner()
    openapi_path = Path(__file__).parent / "3.1_specific.openapi.yaml"
    output_path = Path.cwd() / "test-3-1-features-client"
    snapshots_dir = Path(__file__).parent / "metadata_snapshots"

    for (meta, file, rename_to) in (("setup", "setup.py", "setup.py"), ("pdm", "pyproject.toml", "pdm.pyproject.toml"), ("poetry", "pyproject.toml", "poetry.pyproject.toml")):
        shutil.rmtree(output_path, ignore_errors=True)
        result = runner.invoke(app, ["generate", f"--path={openapi_path}", f"--meta={meta}"])

        if result.stdout:
            print(result.stdout)
        if result.exception:
            raise result.exception

        (output_path / file).rename(snapshots_dir / rename_to)

    shutil.rmtree(output_path, ignore_errors=True)


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


def regen_skip_read_only_golden_record():
    regen(
        "openapi_3.1_skip-read-only.yaml",
        "config-skip-read-only.yml",
        "golden-record-skip-read-only",
        "my-read-only-properties-api-client",
    )


if __name__ == "__main__":
    regen_golden_record()
    regen_golden_record_3_1_features()
    regen_metadata_snapshots()
    regen_custom_template_golden_record()
    regen_literal_enums_golden_record()
    regen_skip_read_only_golden_record()
