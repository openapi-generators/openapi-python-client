---
default: patch
---

# Fall back to schema key when two schemas share a `title`

Tools like FastAPI emit duplicate `title` values for input and output variants of the same model (for example `Thing-Input` and `Thing-Output` both carrying `title: Thing`). The first variant took the title-derived class name and the second was silently dropped with an `Attempted to generate duplicate models` error, along with every endpoint that referenced it.

The second variant now falls back to a class name derived from its schema key (`Thing-Output` becomes `ThingOutput`), so both schemas survive and their endpoints generate.
