---
default: major
---

# Switch from `httpx` to `httpx2` in generated clients

[`httpx2`](https://pydantic.dev/docs/httpx2/get-started/) is largely compatible with `httpx` and should only be a breaking change for users who customize the internal `Client`.

Thanks to @s-sajid-ali and @johnthagen for making this one happen in PR #1461 and discussion #1455!
