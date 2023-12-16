---
default: patch
---

# Always use correct content type for requests

In previous versions, a request body that was similar to a known content type would use that content type in the request. For example `application/json` would be used for `application/vnd.api+json`. This was incorrect and could result in invalid requests being sent.

Now, the content type defined in the OpenAPI document will always be used.
