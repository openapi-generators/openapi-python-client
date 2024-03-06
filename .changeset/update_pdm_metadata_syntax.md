---
default: major
---

# Update PDM metadata syntax

Metadata generated for PDM will now use the new `distribution = true` syntax instead of `package-type = "library"`. 
New packages generated with `--meta pdm` will require PDM `2.12.0` or later to build. 
