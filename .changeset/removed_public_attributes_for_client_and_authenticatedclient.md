---
default: major
---

#### Removed public attributes for `Client` and `AuthenticatedClient`

The following attributes have been removed from `Client` and `AuthenticatedClient`:

- `base_url`—this can now only be set via the initializer
- `cookies`—set at initialization or use `.with_cookies()`
- `headers`—set at initialization or use `.with_headers()`
- `timeout`—set at initialization or use `.with_timeout()`
- `verify_ssl`—this can now only be set via the initializer
- `follow_redirects`—this can now only be set via the initializer
