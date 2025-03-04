---
default: minor
---

# Enumerate duplicate model names

#1212 by @tjb346

This addresses: https://github.com/openapi-generators/openapi-python-client/issues/652

Even with `use_path_prefixes_for_title_model_names` set to `true`, duplicate model class names can occur. By default, when duplicates are encountered they will be skipped. This can cause error when they are referenced later.

This enables setting `enumerate_duplicate_model_names` to `true` (`false` by default) in the config file which will result in a number being added to duplicate names starting with 1. For instance, if there are multiple occurrences in the schema of `MyModelName`, the initial occurrence will remain `MyModelName` and subsequent occurrences will be named `MyModelName1`, `MyModelName2` and so on.
