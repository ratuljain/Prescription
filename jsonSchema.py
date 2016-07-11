
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

chemistSchema = {
    "type": "object",
    "properties" : {
        "pharmacy_name": {"type": "string"},
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "phone_number": {"type": "string"},
        "address": {"type": "string"},
    },
    "required": [
    "first_name",
    "last_name",
    "phone_number",
    "address",
    "pharmacy_name"
  ]
}

orderSchema = {
    "type": "object",
    "properties" : {


    },
    "required": [
    "patient_id",
    "chemist_id",
    "order"
  ]
}

tokenSchema = {
    "type": "object",
    "properties" : {
        "device_id": {"type": "string"},
        "registrationToken": {"type": "string"}
    },
    "required": [
    "device_id",
    "registrationToken"
  ]
}

