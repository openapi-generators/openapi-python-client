---
default: major
---

# Switch from Black to Ruff for formatting

`black` is no longer a runtime dependency, so if you have them set in custom `post_hooks` in a config file, you'll need to make sure they're being installed manually. [`ruff`](https://docs.astral.sh/ruff) is now installed and used by default instead.
