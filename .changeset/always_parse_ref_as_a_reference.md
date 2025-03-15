---
default: patch
---

# Always parse `$ref` as a reference

If additional attributes were included with a `$ref` (for example `title` or `description`), the property could be 
interpreted as a new type instead of a reference, usually resulting in `Any` in the generated code.
Now, any sibling properties to `$ref` will properly be ignored, as per the OpenAPI specification.

Thanks @nkrishnaswami!
