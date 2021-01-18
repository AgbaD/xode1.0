#!/usr/bin/python3
# Author:   @AgbaD | @Agba_dr3

from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError


userLoginSchema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "format": "email"
        },
        "password": {
            "type": "string"
        },
    },
    "required": ["email", "password"],
    "additionalProperties": False
}


def validate_login(user):
    try:
        validate(user, userLoginSchema)
        return {"msg": "success"}
    except SchemaError as e:
        return {"msg": "error", "error": e.message}
    except ValidationError as e:
        return {"msg": "error", "error": e.message}
