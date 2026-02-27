# Summary

Added support for responses with non-standard HTTP Status Codes. Off by default, enabled with `allow_int_response_codes`.

# Problem

Currently if a response with a status code that does not exist in `http.HTTPStatusCode` a `ValueError` is raised. For example: `ValueError: 490 is not a valid HTTPStatus`.

# Edge Case

If a non-standard status code is received from an endpoint that doesn't define any responses with non-standard status codes the old behavior will appear.
