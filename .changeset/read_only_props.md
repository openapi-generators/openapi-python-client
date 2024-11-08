---
default: minor
---

# Omitting `readOnly` properties from request bodies

OpenAPI allows any object property to be marked as `readOnly: true`, meaning that the server does not allow that property to be updated in a request. OpenAPI does not specifically define "updated", but some servers may interpret it to mean that no value should be serialized for the property at all.

You can now tell `openapi-python-client` to omit read-only properties when serializing a schema, if and only if it is being serialized as part of a request body. This behavior is only enabled if you set `skip_sending_read_only_properties: true` in your configuration.

Regardless of this option, read-only properties will still be deserialized normally in responses, and the behavior of the object's `to_dict` method is unchanged in all other contexts.
