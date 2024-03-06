---
default: patch
---

# Allow hyphens in path parameters

Before now, path parameters which were invalid Python identifiers were not allowed, and would fail generation with an
"Incorrect path templating" error. In particular, this meant that path parameters with hyphens were not allowed.
This has now been fixed!

PR #986 fixed issue #976. Thanks @harabat!

> [!WARNING]
> This change may break custom templates, see [this diff](https://github.com/openapi-generators/openapi-python-client/pull/986/files#diff-0de8437b26075d8fe8454cf47d8d95d4835c7f827fa87328e03f690412be803e)
> if you have trouble upgrading.
