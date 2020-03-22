""" Regenerate golden-master """
import shutil
from pathlib import Path

from typer.testing import CliRunner

from openapi_python_client.cli import app

if __name__ == "__main__":
    runner = CliRunner()
    openapi_path = Path(__file__).parent / "fastapi" / "openapi.json"
    gm_path = Path(__file__).parent / "golden-master"
    shutil.rmtree(gm_path)
    output_path = Path.cwd() / "my-test-api-client"

    runner.invoke(app, ["generate", f"--path={openapi_path}"])

    output_path.rename(gm_path)
