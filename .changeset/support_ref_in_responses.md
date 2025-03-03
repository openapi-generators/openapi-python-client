---
default: major
---

# Support `$ref` in responses

Previously, using a `$ref` to define a response was ignored, the code to call the endpoint was still generated, but 
the response would not be parsed. Now, responses defined with `$ref` will be used to generate the response model, which 
will parse the response at runtime.

If a `$ref` is incorrect or uses a feature that is not supported by the generator, these endpoints will start failing to 
generate.
