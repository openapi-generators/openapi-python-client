---
default: patch
---

# Fix optional bodies

If a body is not required (the default), it will now:

1. Have `Unset` as part of its type annotation.
2. Default to a value of `UNSET`
3. Not be included in the request if it is `UNSET`

Thanks @orelmaliach for the report! Fixes #1354
