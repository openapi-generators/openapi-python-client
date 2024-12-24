---
default: patch
---

# Fix compatibility with Pydantic 2.10+

#1176 by @Viicos

Set `defer_build` to models that we know will fail to build, and call `model_rebuild`
in the `__init__.py` file.
