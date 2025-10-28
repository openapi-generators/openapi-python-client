---
default: minor
---

# Upgrade generated clients to 3.10 union syntax

All generated types now use the `A | B` syntax instead of `Union[A, B]` or `Optional[A]`.
