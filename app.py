import itertools

from flask import Flask, jsonify, abort, make_response, request
from jsonschema import validate
from playhouse.shortcuts import *

import models
from jsonSchema import doctorSchema

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
    return jsonify({'doctors': l})


@app.route('/Prescription/api/v1.0/doctors/<int:doctor_id>', methods=['GET'])
def getDoc(doctor_id):
    try:
        doc = models.Doctor.getDoctor(doctor_id)
        return jsonify({'doctors': (model_to_dict(doc))})
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



if __name__ == '__main__':
    # models.initialize()
    app.run(debug=True)
