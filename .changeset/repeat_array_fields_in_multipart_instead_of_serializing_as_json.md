---
default: major
---

# Change default multipart array serialization

Previously, any arrays of values in a `multipart/form-data` body would be serialized as an `application/json` part.
This matches the default behavior specified by OpenAPI and supports arrays of files (`binary` format strings).
However, because this generator doesn't yet support specifying `encoding` per property, this may result in 
now-incorrect code when the encoding _was_ explicitly set to `application/json` for arrays of scalar values.

PR #938 fixes #692. Thanks @micha91 for the fix, @ratgen and @FabianSchurig for testing, and @davidlizeng for the original report... many years ago 😅.
