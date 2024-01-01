---
default: patch
---

# Do not stop generation for invalid enum values

This generator only supports `enum` values that are strings or integers. 
Previously, this was handled at the parsing level, which would cause the generator to fail if there were any unsupported values in the document.
Now, the generator will correctly keep going, skipping only endpoints which contained unsupported values.

Thanks for reporting #922 @macmoritz!
