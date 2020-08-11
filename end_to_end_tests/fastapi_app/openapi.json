{
    "openapi": "3.0.2",
    "info": {
        "title": "My Test API",
        "description": "An API for testing openapi-python-client",
        "version": "0.1.0"
    },
    "paths": {
        "/ping": {
            "get": {
                "summary": "Ping",
                "description": "A quick check to see if the system is running ",
                "operationId": "ping_ping_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "title": "Response Ping Ping Get",
                                    "type": "boolean"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/tests/": {
            "get": {
                "tags": [
                    "tests"
                ],
                "summary": "Get List",
                "description": "Get a list of things ",
                "operationId": "getUserList",
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "title": "An Enum Value",
                            "type": "array",
                            "items": {
                                "$ref": "#/components/schemas/AnEnum"
                            }
                        },
                        "name": "an_enum_value",
                        "in": "query"
                    },
                    {
                        "required": true,
                        "schema": {
                            "title": "Some Date",
                            "anyOf": [
                                {
                                    "type": "string",
                                    "format": "date"
                                },
                                {
                                    "type": "string",
                                    "format": "date-time"
                                }
                            ]
                        },
                        "name": "some_date",
                        "in": "query"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "title": "Response Get List Tests  Get",
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/components/schemas/AModel"
                                    }
                                }
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/tests/upload": {
            "post": {
                "tags": [
                    "tests"
                ],
                "summary": "Upload File",
                "description": "Upload a file ",
                "operationId": "upload_file_tests_upload_post",
                "parameters": [
                    {
                        "required": false,
                        "schema": {
                            "title": "Keep-Alive",
                            "type": "boolean"
                        },
                        "name": "keep-alive",
                        "in": "header"
                    }
                ],
                "requestBody": {
                    "content": {
                        "multipart/form-data": {
                            "schema": {
                                "$ref": "#/components/schemas/Body_upload_file_tests_upload_post"
                            }
                        }
                    },
                    "required": true
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/tests/json_body": {
            "post": {
                "tags": [
                    "tests"
                ],
                "summary": "Json Body",
                "description": "Try sending a JSON body ",
                "operationId": "json_body_tests_json_body_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/AModel"
                            }
                        }
                    },
                    "required": true
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    "components": {
        "schemas": {
            "AModel": {
                "title": "AModel",
                "required": [
                    "an_enum_value",
                    "aCamelDateTime",
                    "a_date"
                ],
                "type": "object",
                "properties": {
                    "an_enum_value": {
                        "$ref": "#/components/schemas/AnEnum"
                    },
                    "nested_list_of_enums": {
                        "title": "Nested List Of Enums",
                        "type": "array",
                        "items": {
                            "type": "array",
                            "items": {
                                "$ref": "#/components/schemas/DifferentEnum"
                            }
                        },
                        "default": []
                    },
                    "some_dict": {
                        "title": "Some Dict",
                        "type": "object",
                        "additionalProperties": {
                            "type": "string"
                        },
                        "default": {}
                    },
                    "aCamelDateTime": {
                        "title": "Acameldatetime",
                        "anyOf": [
                            {
                                "type": "string",
                                "format": "date-time"
                            },
                            {
                                "type": "string",
                                "format": "date"
                            }
                        ]
                    },
                    "a_date": {
                        "title": "A Date",
                        "type": "string",
                        "format": "date"
                    }
                },
                "description": "A Model for testing all the ways custom objects can be used "
            },
            "AnEnum": {
                "title": "AnEnum",
                "enum": [
                    "FIRST_VALUE",
                    "SECOND_VALUE"
                ],
                "description": "For testing Enums in all the ways they can be used "
            },
            "Body_upload_file_tests_upload_post": {
                "title": "Body_upload_file_tests_upload_post",
                "required": [
                    "some_file"
                ],
                "type": "object",
                "properties": {
                    "some_file": {
                        "title": "Some File",
                        "type": "string",
                        "format": "binary"
                    }
                }
            },
            "DifferentEnum": {
                "title": "DifferentEnum",
                "enum": [
                    "DIFFERENT",
                    "OTHER"
                ],
                "description": "An enumeration."
            },
            "HTTPValidationError": {
                "title": "HTTPValidationError",
                "type": "object",
                "properties": {
                    "detail": {
                        "title": "Detail",
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/ValidationError"
                        }
                    }
                }
            },
            "ValidationError": {
                "title": "ValidationError",
                "required": [
                    "loc",
                    "msg",
                    "type"
                ],
                "type": "object",
                "properties": {
                    "loc": {
                        "title": "Location",
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "msg": {
                        "title": "Message",
                        "type": "string"
                    },
                    "type": {
                        "title": "Error Type",
                        "type": "string"
                    }
                }
            }
        }
    }
}