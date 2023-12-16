---
default: major
---

# Renamed body types and parameters

PR #900 addresses #822.

Where previously there would be one body parameter per supported content type, now there is a single `body` parameter which takes a union of all the possible inputs. This correctly models the fact that only one body can be sent (and ever would be sent) in a request.

For example, when calling a generated endpoint, code which used to look like this:

```python
post_body_multipart.sync_detailed(
    client=client,
    multipart_data=PostBodyMultipartMultipartData(),
)
```

Will now look like this:

```python
post_body_multipart.sync_detailed(
    client=client,
    body=PostBodyMultipartBody(),
)
```

Note that both the input parameter name _and_ the class name have changed. This should result in simpler code when there is only a single body type and now produces correct code when there are multiple body types.
