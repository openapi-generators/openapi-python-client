---
default: minor
---

# Add `--meta=pdm` option for generating PEP621 + PDM metadata

The default metadata is still `--meta=poetry`, which generates a `pyproject.toml` file with Poetry-specific metadata.
This change adds the `--meta=pdm` option which includes [PDM](https://pdm-project.org/latest/)-specific metadata, but also 
standard [PEP621](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#writing-pyproject-toml)
metadata. This may be useful as a starting point for other dependency managers & build tools (like Hatch).
