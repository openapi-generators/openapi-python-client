---
default: minor
---

# Added an `--output-path` option to `generate`

Rather than changing directories before running `generate` you can now specify an output directory with `--output-path`.
Note that the project name will _not_ be appended to the `--output-path`, whatever path you specify is where the 
generated code will be placed.
