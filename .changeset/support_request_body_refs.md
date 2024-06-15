---
default: minor
---

# Support request body refs

You can now define and reuse bodies via refs, with a document like this:

```yaml
paths:
  /something:
    post:
      requestBody:
        "$ref": "#/components/requestBodies/SharedBody"
components:
  requestBodies:
    SharedBody:
      content:
        application/json:
          schema:
            type: string
```

Thanks to @kigawas and @supermihi for initial implementations and @RockyMM for the initial request.

Closes #633, closes #664, resolves #595.
