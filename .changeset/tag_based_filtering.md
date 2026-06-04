---
default: minor
---

# Add `include_tags` / `exclude_tags` to filter generated endpoints by tag

Endpoints can now be limited to (or excluded by) OpenAPI tags via the `include_tags` / `exclude_tags` config keys or the `--include-tags` / `--exclude-tags` CLI options. Schemas that become unused after filtering are pruned automatically.
