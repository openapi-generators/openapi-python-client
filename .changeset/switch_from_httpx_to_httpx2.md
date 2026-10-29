---
default: major
---

# Switch from httpx to httpx2

For better or worse, httpx has not been actively maintained and hasn't seen a stable release in years. The Pydantic
org forked this into httpx and took over maintenance. The fork maintains API compatibility with the latest stable httpx
releast 0.28.1.

Hypothetically httpx might see a 1.0 release at some point, I am not sure about the plans for that, even that doesn't
seem to be seeing much activity. Given the potential sensitivity of the generated clients, switching to a more-actively
maintained HTTP client library, including its switch to defaulting to the hopefully-better-updated system certificate
store, given recent issues with web PKI, is prudent.

This generates all usages of httpx2 with `import httpx2 as httpx` rather than importing directly and changing all of
the use sites. This method is endorsed by the httpx2 migration guide and keeps things simpler and does not change any
of the existing API. The primary way this could break usage is for consumers that rely on this package bringing in
httpx as a dependency.
