---
default: minor
---

# Support all `text/*` content types in responses

Within an API response, any content type which starts with `text/` will now be treated the same as `text/html` already was—they will return the `response.text` attribute from the [httpx Response](https://www.python-httpx.org/api/#response).

Thanks to @fdintino for the initial implementation, and thanks for the discussions from @kairntech, @rubenfiszel, and @antoneladestito.

Closes #797 and #821.
