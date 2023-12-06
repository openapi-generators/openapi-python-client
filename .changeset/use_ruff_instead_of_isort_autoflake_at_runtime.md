---
default: major
---

#### Use Ruff instead of isort + autoflake at runtime

`isort` and `autoflake` are no longer runtime dependencies, so if you have them set in custom `post_hooks` in a config file, you'll need to make sure they're being installed manually. [`ruff`](https://docs.astral.sh/ruff) is now installed and used by default instead.
