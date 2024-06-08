---
default: major
---

# Removed the `update` command

The `update` command is no more, you can (mostly) replace its usage with some new flags on the `generate` command.

If you had a package named `my-api-client` in the current working directory, the `update` command previously would update the `my_api_client` module within it. You can now _almost_ perfectly replicate this behavior using `openapi-python-client generate --meta=none --output-path=my-api-client/my_api_client --overwrite`.

The only difference is that `my-api-client` would have run `post_hooks` in the `my-api-client` directory, 
but `generate` will run `post_hooks` in the `output-path` directory.

Alternatively, you can now also run `openapi-python-client generate --meta=<your-meta-type> --overwrite` to regenerate 
the entire client, if you don't care about keeping any changes you've made to the generated client.

Please comment on [discussion #826](https://github.com/openapi-generators/openapi-python-client/discussions/826)
(or a new discussion, as appropriate) to aid in designing future features that fill any gaps this leaves for you.
