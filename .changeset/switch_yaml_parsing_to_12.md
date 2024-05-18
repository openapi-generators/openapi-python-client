---
default: major
---

# Switch YAML parsing to 1.2

This change switches the YAML parsing library to `ruamel.yaml` which follows the YAML 1.2 specification. 
[There are breaking changes](https://yaml.readthedocs.io/en/latest/pyyaml/#defaulting-to-yaml-12-support) from YAML 1.1 to 1.2,
though they will not affect most use cases.

PR #1042 fixes #1041. Thanks @rtaycher!
