---
default: major
---

# Removed ability to set an array as a multipart body

Previously, when defining a request's body as `multipart/form-data`, the generator would attempt to generate code 
for both `object` schemas and `array` schemas. However, most arrays could not generate valid multipart bodies, as 
there would be no field names (required to set the `Content-Disposition` headers).

The code to generate any body for `multipart/form-data` where the schema is `array` has been removed, and any such 
bodies will be skipped. This is not _expected_ to be a breaking change in practice, since the code generated would 
probably never work.

If you have a use-case for `multipart/form-data` with an `array` schema, please [open a new discussion](https://github.com/openapi-generators/openapi-python-client/discussions) with an example schema and the desired functional Python code.
