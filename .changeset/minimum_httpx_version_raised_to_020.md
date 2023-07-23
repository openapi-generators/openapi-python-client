---
default: major
---

#### Minimum httpx version raised to 0.20

Some features of generated clients already failed at runtime when using httpx < 0.20, but now the minimum version is enforced at generation time.
