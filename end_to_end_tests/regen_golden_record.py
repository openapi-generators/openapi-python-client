""" Regenerate golden-record """
import filecmp
import os
import shutil
import tempfile
from pathlib import Path

from typer.testing import CliRunner

from openapi_python_client.cli import app


def regen_golden_record():
    runner = CliRunner()
    openapi_path = Path(__file__).parent / "openapi.json"

    gr_path = Path(__file__).parent / "golden-record"
    output_path = Path.cwd() / "my-test-api-client"
    config_path = Path(__file__).parent / "config.yml"

    shutil.rmtree(gr_path, ignore_errors=True)
    shutil.rmtree(output_path, ignore_errors=True)

    result = runner.invoke(app, ["generate", f"--config={config_path}", f"--path={openapi_path}"])

    if result.stdout:
        print(result.stdout)
    if result.exception:
        raise result.exception
    output_path.rename(gr_path)


def regen_custom_template_golden_record():
    runner = CliRunner()
    openapi_path = Path(__file__).parent / "openapi.json"
    tpl_dir = Path(__file__).parent / "test_custom_templates"

    gr_path = Path(__file__).parent / "golden-record"
    tpl_gr_path = Path(__file__).parent / "custom-templates-golden-record"

    output_path = Path(tempfile.mkdtemp())
    config_path = Path(__file__).parent / "config.yml"

    shutil.rmtree(tpl_gr_path, ignore_errors=True)

    os.chdir(str(output_path.absolute()))
    result = runner.invoke(
        app, ["generate", f"--config={config_path}", f"--path={openapi_path}", f"--custom-template-path={tpl_dir}"]
    )

    if result.stdout:
        generated_output_path = output_path / "my-test-api-client"
        for f in generated_output_path.glob("**/*"):  # nb: works for Windows and Unix
            relative_to_generated = f.relative_to(generated_output_path)
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
    regen_custom_template_golden_record()
