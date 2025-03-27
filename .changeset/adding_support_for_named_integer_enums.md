---
default: minor
---

# Adding support for named integer enums

#1214 by @barrybarrette

Adding support for named integer enums via an optional extension, `x-enum-varnames`. 

This extension is added to the schema inline with the `enum` definition:
```
"MyEnum": {
    "enum": [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        99
    ],
    "type": "integer",
    "format": "int32",
    "x-enum-varnames": [
        "Deinstalled",
        "Installed",
        "Upcoming_Site",
        "Lab_Site",
        "Pending_Deinstall",
        "Suspended",
        "Install_In_Progress",
        "Unknown"
    ]
}
```

The result:
![image](https://github.com/user-attachments/assets/780880b3-2f1f-49be-823b-f9abb713a3e1)
