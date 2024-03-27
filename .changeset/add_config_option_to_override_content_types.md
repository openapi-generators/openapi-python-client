---
default: minor
---

# Add config option to override content types

You can now define a `content_type_overrides` field in your `config.yml`:

```yaml
content_type_overrides:
  application/zip: application/octet-stream
```

This allows `openapi-python-client` to generate code for content types it doesn't recognize.

PR #1010 closes #810. Thanks @gaarutyunov!
