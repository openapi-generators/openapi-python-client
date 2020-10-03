""" Regenerate golden-record """
import shutil
from pathlib import Path

from typer.testing import CliRunner

from openapi_python_client.cli import app

if __name__ == "__main__":
    runner = CliRunner()
    openapi_path = Path(__file__).parent / "openapi.json"
    gr_path = Path(__file__).parent / "golden-record"
    shutil.rmtree(gr_path, ignore_errors=True)
    output_path = Path.cwd() / "my-test-api-client"
    shutil.rmtree(output_path, ignore_errors=True)
    config_path = Path(__file__).parent / "config.yml"

    result = runner.invoke(app, [f"--config={config_path}", "generate", f"--path={openapi_path}"])
    if result.stdout:
        print(result.stdout)
    if result.exception:
        raise result.exception
    output_path.rename(gr_path)
