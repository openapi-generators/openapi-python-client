---
default: minor
---

# Add per-request headers, timeout, and auth overrides to endpoint functions

All generated endpoint functions (`sync_detailed`, `asyncio_detailed`, `sync`, `asyncio`) now accept three optional keyword arguments forwarded directly to the underlying httpx request:

- `headers: dict[str, str] | None = None` — extra headers merged on top of any spec-defined headers for this request
- `timeout: httpx.Timeout | None | Unset = UNSET` — override the client-level timeout for this request; `None` disables the timeout
- `auth: httpx.Auth | None | Unset = UNSET` — override the client-level auth for this request; `None` disables auth

This allows per-request customisation without creating a new client instance, preserving the shared httpx connection pool. Using `with_headers()` / `with_timeout()` at runtime was previously the only option, but those methods mutate the original client's underlying httpx client as a side effect and cause the returned client to open a new connection pool on first use—making them unsafe for concurrent async code.

Note: client-level headers cannot be fully removed for a single request via this mechanism, only overridden with a different value.
