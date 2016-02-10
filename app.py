import itertools
import json

from bson import json_util
import models
from flask import Flask, jsonify, abort, make_response, request
from jsonSchema import doctorSchema, patientSchema
from jsonschema import validate
from playhouse.shortcuts import *

app = Flask(__name__)

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

def dictfetchall(cursor):
    """Returns all rows from a cursor as a list of dicts"""
    desc = cursor.description
    return [dict(itertools.izip([col[0] for col in desc], row))
            for row in cursor.fetchall()]


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'URL not found'}), 400)


@app.errorhandler(409)
def not_found(error):
    return make_response(jsonify({'error': 'Phone number already exists'}), 409)


@app.route('/', methods=['GET'])
def index():
    return "Welcome to da API, mah lyf mah rulz"


# gets json of every doctor in the table

@app.route('/Prescription/api/v1.0/doctors', methods=['GET'])
def getDocList():
    every_doc_row = models.Doctor.getAllDoctor()
    l = []
    for i in every_doc_row:
        l.append(model_to_dict(i))
    x = json.dumps(l, default=json_util.default)
    return jsonify({'doctors': json.loads(x)})


# gets json of a doctor with the provided id in the table

@app.route('/Prescription/api/v1.0/doctors/<int:doctor_id>', methods=['GET'])
def getDoc(doctor_id):
    try:
        doc = models.Doctor.getDoctor(doctor_id)
        x = json.dumps(model_to_dict(doc), default=json_util.default)
        return jsonify({'doctors': json.loads(x)})
    except:
        abort(404)


# adds a doctor to the table if the input is given in a json

@app.route('/Prescription/api/v1.0/doctors', methods=['POST'])
def addDoc():
    try:
        validate(request.json, doctorSchema)
    except:
        abort(400)

    try:
        models.Doctor.addDoctor(request.json)
    except IntegrityError:
        abort(409)

    return jsonify({'doctor': request.json}), 201


# gets json of every Patient in the table

# curl -i -H "Content-Type: application/json" -X POST
# -d '{  "first_name": "Saurabh",  "last_name": "Arora",  "phone_number": "9584365553"}'
# http://127.0.0.1:5000/Prescription/api/v1.0/doctors

@app.route('/Prescription/api/v1.0/patients', methods=['GET'])
def getPatientList():
    every_patient_row = models.Patient.getAllPatient()

    l = []
    for i in every_patient_row:
        l.append(model_to_dict(i))
    x = json.dumps(l, default=json_util.default)

    return jsonify({'patients': json.loads(x)})


# gets json of a patient with the provided id in the table


@app.route('/Prescription/api/v1.0/patients/<int:patient_id>', methods=['GET'])
def getPatient(patient_id):
    try:
        patient = models.Patient.getPatient(patient_id)
        x = json.dumps(model_to_dict(patient), default=json_util.default)
        return jsonify({'patients': json.loads(x)})
    except:
        abort(404)


# adds a patient to the table if the input is given in a json


@app.route('/Prescription/api/v1.0/patients', methods=['POST'])
def addPatient():
    try:
        validate(request.json, patientSchema)
    except:
        abort(400)

    try:
        models.Patient.addPatient(request.json)
    except IntegrityError:
        abort(409)

    return jsonify({'patient': request.json}), 201


# gets a json of all prescriptions prescribed to a patient

@app.route('/Prescription/api/v1.0/prescription/all/<int:patient_id>', methods=['GET'])
def getEveryPrescription(patient_id):
    try:
        prescription = models.Prescription.getEveryPrescription(patient_id)
        x = json.dumps(prescription, default=date_handler)
        return jsonify({'Prescription': json.loads(x)})
    except:
        abort(404)


# gets latest prescriptions prescribed to a patient

@app.route('/Prescription/api/v1.0/prescription/<int:patient_id>', methods=['GET'])
def getLatestPrescription(patient_id):
    try:
        prescription = models.Prescription.getLatestPrescription(patient_id)
        x = json.dumps(prescription, default=json_util.default)
        return jsonify({'Prescription': json.loads(x)})
    except:
        abort(404)


# adds a prescription to a patient

@app.route('/Prescription/api/v1.0/prescription/<int:patient_id>', methods=['POST'])
def addPrescription(patient_id):
    try:
        x = json.dumps(request.json)   #converting dict to a string, was
                                       # being stored as a unicode and was not able to be parsed by JAVA
        models.Prescription.addPrescription(patient_id, x)
    except IntegrityError:
        abort(400)

    return jsonify({'Prescription': request.json}), 201


if __name__ == '__main__':
    models.initialize()
    app.run(debug=True)
