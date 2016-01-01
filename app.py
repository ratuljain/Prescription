import itertools
import json

from bson import json_util
import models
from flask import Flask, jsonify, abort, make_response, request
from jsonSchema import doctorSchema, patientSchema
from jsonschema import validate
from playhouse.shortcuts import *

app = Flask(__name__)


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


@app.route('/Prescription/api/v1.0/doctors', methods=['GET'])
def getDocList():
    every_doc_row = models.Doctor.getAllDoctor()
    l = []
    for i in every_doc_row:
        l.append(model_to_dict(i))
    x = json.dumps(l, default=json_util.default)
    return jsonify({'doctors': json.loads(x)})


@app.route('/Prescription/api/v1.0/doctors/<int:doctor_id>', methods=['GET'])
def getDoc(doctor_id):
    try:
        doc = models.Doctor.getDoctor(doctor_id)
        x = json.dumps(model_to_dict(doc), default=json_util.default)
        return jsonify({'doctors': json.loads(x)})
    except:
        abort(404)


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

@app.route('/Prescription/api/v1.0/patients', methods=['GET'])
def getPatientList():
    every_patient_row = models.Patient.getAllPatient()

    l = []
    for i in every_patient_row:
        l.append(model_to_dict(i))
    x = json.dumps(l, default=json_util.default)

    return jsonify({'patients': json.loads(x)})

@app.route('/Prescription/api/v1.0/patients/<int:patient_id>', methods=['GET'])
def getPatient(patient_id):
    try:
        patient = models.Patient.getPatient(patient_id)
        x = json.dumps(model_to_dict(patient), default=json_util.default)
        return jsonify({'patients': json.loads(x)})
    except:
        abort(404)


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


@app.route('/Prescription/api/v1.0/prescription/all/<int:patient_id>', methods=['GET'])
def getEveryPrescription(patient_id):
    try:
        prescription = models.Prescription.getEveryPrescription(patient_id)
        x = json.dumps(prescription, default=json_util.default)
        return jsonify({'Prescription': json.loads(x)})
    except:
        abort(404)


@app.route('/Prescription/api/v1.0/prescription/<int:patient_id>', methods=['GET'])
def getLatestPrescription(patient_id):
    try:
        prescription = models.Prescription.getLatestPrescription(patient_id)
        x = json.dumps(prescription, default=json_util.default)
        return jsonify({'Prescription': json.loads(x)})
    except:
        abort(404)


@app.route('/Prescription/api/v1.0/prescription/<int:patient_id>', methods=['POST'])
def addPrescription(patient_id):

    try:
        models.Prescription.addPrescription(patient_id, request.json)
    except IntegrityError:
        abort(400)

    return jsonify({'Prescription': request.json}), 201

if __name__ == '__main__':
    models.initialize()
    app.run(debug=True)
