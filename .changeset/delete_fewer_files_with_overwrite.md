---
default: major
---

# Delete fewer files with `--overwrite`

`--overwrite` will no longer delete the entire output directory before regenerating. Instead, it will only delete 
specific, known directories within that directory. Right now, that is only the generated `models` and `api` directories.

Other generated files, like `README.md`, will be overwritten. Extra files and directories outside of those listed above 
will be left untouched, so you can any extra modules or files around while still updating `pyproject.toml` automatically.

Closes #1105.
