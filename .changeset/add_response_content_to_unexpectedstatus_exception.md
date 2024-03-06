---
default: minor
---

# Add response content to `UnexpectedStatus` exception

The error message for `UnexpectedStatus` exceptions will now include the UTF-8 decoded (ignoring errors) body of the response.

PR #989 implements #840. Thanks @harabat!
