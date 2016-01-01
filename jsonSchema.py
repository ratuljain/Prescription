from jsonschema import validate

doctorSchema = {
    "type": "object",
    "properties" : {
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "phone_number": {"type": "string"}
    },
    "required": [
    "first_name",
    "last_name",
    "phone_number"
  ]
}

patientSchema = {
    "type": "object",
    "properties" : {
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "phone_number": {"type": "string"}
    },
    "required": [
    "first_name",
    "last_name",
    "phone_number"
  ]
}

