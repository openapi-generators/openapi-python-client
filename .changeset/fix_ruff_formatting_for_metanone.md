---
default: patch
---

# Fix Ruff formatting for `--meta=none`

PR #940 fixes issue #939. Thanks @satwell!

Due to the lack of `pyproject.toml`, Ruff was not getting configured properly when `--meta=none`.
As a result, it didn't clean up common generation issues like duplicate imports, which would then cause errors from 
linters.

This is now fixed by changing the default `post_hook` to `ruff check . --fix --extend-select=I` when `--meta=none`.
