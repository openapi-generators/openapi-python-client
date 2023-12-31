---
default: minor
---

# Support multiple possible `requestBody`

PR #900 addresses #822.

It is now possible in some circumstances to generate valid code for OpenAPI documents which have multiple possible `requestBody` values. Previously, invalid code could have been generated with no warning (only one body could actually be sent).

Only one content type per "category" is currently supported at a time. The categories are:

- JSON, like `application/json`
- Binary data, like `application/octet-stream`
- Encoded form data, like `application/x-www-form-urlencoded`
- Files, like `multipart/form-data`
