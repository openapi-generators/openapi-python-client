---
default: major
---

#### `AuthenticatedClient` no longer inherits from `Client`

The API of `AuthenticatedClient` is still a superset of `Client`, but the two classes no longer share a common base class.
