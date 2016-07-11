import itertools
import json
import models
from flask import Flask, jsonify, abort, make_response, request
from jsonSchema import doctorSchema, patientSchema, chemistSchema, orderSchema, tokenSchema
from jsonschema import validate
from oauth2client import client, crypt

from playhouse.shortcuts import *

import gcmTest


app = Flask(__name__)

WEB_CLIENT_ID = "123945801611-k2sqmjukigvua9t2nhsb6a0lfluqneth.apps.googleusercontent.com"
ANDROID_CLIENT_ID = "123945801611-4lgogdbao7bps4k1kqhidn3b27t30bbo.apps.googleusercontent.com"
APIKey = "AIzaSyBwp1_iKvFIH9FFTSv65sRUQejTh0TkqnY"
# reg_id = 'eprzyGWpkZQ:APA91bEbPwEhK2mMnkpHY9MR3oLcH4MXF38VLgglpNePHjceathTOiOyYXg-Khu5Ryp5-PbFU9B3Gf8FdE23Tn_yDGFQdFDGm3dljhtFnznylU3Ndw3zCB6r3pldjdlGSAiRP1D6kU-J'
reg_id = "cywq8GyZDP0:APA91bHD46xaSwKXVIyX0OEQApnqKIUTC9-8UltNDIfE2ocvHLpq4jK0yROYfVvAuW5veeFHYO8XTABZrpWrlO3vwLbciSNxzXuuJG1GvheqibqWdUEZeJtSlof3KyS8vuLap3HQUf8Y"

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

def dictfetchall(cursor):
    """Returns all rows from a cursor as a list of dicts"""
    desc = cursor.description
    return [dict(itertools.izip([col[0] for col in desc], row))
            for row in cursor.fetchall()]

def process(i):
    pdetails = {}

    pdetails["phone"] = i['patient_id']['phone_number']
    pdetails["first_name"] = i['patient_id']['first_name']
    pdetails["last_name"] = i['patient_id']['last_name']
    pdetails["address"] = i['patient_id']['address']
    pdetails["time"] = i['timestamp']

    pdetails["order"] = i['order']
    pdetails["orderID"] = i['id']

    return pdetails

def googleTokenValidation(token, WEB_CLIENT_ID, ANDROID_CLIENT_ID):
    try:
        idinfo = client.verify_id_token(token, WEB_CLIENT_ID)
        # print idinfo
        # If multiple clients access the backend server:
        if idinfo['aud'] not in [ANDROID_CLIENT_ID, WEB_CLIENT_ID]:
            raise crypt.AppIdentityError("Unrecognized client.")
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")
        return idinfo
    except crypt.AppIdentityError:
        print "The token is invalid"

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
    print every_doc_row
    l = []
    for i in every_doc_row:
        l.append(model_to_dict(i))
    x = json.dumps(l, default=date_handler)
    return jsonify({'doctors': json.loads(x)})


# gets json of a doctor with the provided id in the table

@app.route('/Prescription/api/v1.0/doctors/<int:doctor_id>', methods=['GET'])
def getDoc(doctor_id):
    try:
        doc = models.Doctor.getDoctor(doctor_id)
        x = json.dumps(model_to_dict(doc), default=date_handler)
        return jsonify({'doctors': json.loads(x)})
    except Exception as e:
        print(e)
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
    except Exception as e:
        print(e)
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
    x = json.dumps(l, default=date_handler)

    return jsonify({'patients': json.loads(x)})


# gets json of a patient with the provided id in the table


@app.route('/Prescription/api/v1.0/patients/<int:patient_id>', methods=['GET'])
def getPatient(patient_id):
    try:
        patient = models.Patient.getPatient(patient_id)
        x = json.dumps(model_to_dict(patient), default=date_handler)
        return jsonify({'patients': json.loads(x)})
    except Exception as e:
        print(e)
        abort(404)


# adds a patient to the table if the input is given in a json


@app.route('/Prescription/api/v1.0/patients', methods=['POST'])
def addPatient():
    try:
        validate(request.json, patientSchema)
    except Exception as e:
        print(e)
        abort(400)

    try:
        models.Patient.addPatient(request.json)
    except Exception as e:
        print(e)
        abort(409)

    return jsonify({'patients': request.json}), 201


@app.route('/Prescription/api/v1.0/patients/<int:patient_id>', methods=['POST'])
def addPatientInfo(patient_id):
    print request.json
    models.Patient.addInfo(request.json, patient_id)

    return jsonify({'patients': request.json}), 201

#######chemists########

@app.route('/Prescription/api/v1.0/chemists', methods=['GET'])
def getChemistList():
    every_chemist_row = models.Chemist.getAllChemist()

    l = []
    for i in every_chemist_row:
        l.append(model_to_dict(i))
    x = json.dumps(l, default=date_handler)

    return jsonify({'chemists': json.loads(x)})


# gets json of a chemist with the provided id in the table


@app.route('/Prescription/api/v1.0/chemists/<int:chemist_id>', methods=['GET'])
def getChemist(chemist_id):
    try:
        chemist = models.Chemist.getChemist(chemist_id)
        x = json.dumps(model_to_dict(chemist), default=date_handler)
        return jsonify({'chemists': json.loads(x)})
    except Exception as e:
        print(e)
        abort(404)


# adds a chemist to the table if the input is given in a json


@app.route('/Prescription/api/v1.0/chemists', methods=['POST'])
def addChemist():
    try:
        validate(request.json, chemistSchema)
    except:
        abort(400)

    try:
        models.Chemist.addChemist(request.json)
    except Exception as e:
        print(e)
        abort(409)

    return jsonify({'chemists': request.json}), 201



# gets a json of all prescriptions prescribed to a patient

@app.route('/Prescription/api/v1.0/prescription/all/<int:patient_id>', methods=['GET'])
def getEveryPrescription(patient_id):
    try:
        prescription = models.Prescription.getEveryPrescription(patient_id)
        x = json.dumps(prescription, default=date_handler)
        return jsonify({'Prescription': json.loads(x)})
    except Exception as e:
        print(e)
        abort(404)


# gets latest prescriptions prescribed to a patient

@app.route('/Prescription/api/v1.0/prescription/<int:patient_id>', methods=['GET'])
def getLatestPrescription(patient_id):
    try:
        prescription = models.Prescription.getLatestPrescription(patient_id)
        x = json.dumps(prescription, default=date_handler)
        data = {'message': 'You have a new order'}
        y = json.dumps((json.loads(x)))
        data['message'] = y
        gcmTest.sendNotification(APIKey, reg_id, data)
        return jsonify({'Prescription': json.loads(x)})
    except Exception as e:
        print(e)
        abort(404)


# adds a prescription to a patient

@app.route('/Prescription/api/v1.0/prescription/<int:patient_id>', methods=['POST'])
def addPrescription(patient_id):
    try:
        x = json.dumps(request.json)   #converting dict to a string, was
                                       # being stored as a unicode and was not able to be parsed by JAVA
        models.Prescription.addPrescription(patient_id, x)
    except Exception as e:
        print(e)
        abort(400)

    return jsonify({'Prescription': request.json}), 201


#######orders########

# gets all open orders for a chemist


@app.route('/Prescription/api/v1.0/orders/open/chemist=<int:chemist_id>', methods=['GET'])
def getChemistOpenOrders(chemist_id):
    try:
        orders = models.Order.getAllOpenOrdersforChemist(chemist_id)

        pList = []
        for i in orders:
            pList.append(process(i))

        x = json.dumps(pList, default=date_handler)
        return jsonify({'Orders': json.loads(x)})

    except Exception as e:
        print(e)
        abort(404)

# gets all closed orders for a chemist
@app.route('/Prescription/api/v1.0/orders/closed/chemist=<int:chemist_id>', methods=['GET'])
def getChemistClosedOrders(chemist_id):
    try:
        orders = models.Order.getAllClosedOrdersforChemist(chemist_id)

        pList = []
        for i in orders:
            pList.append(process(i))

        x = json.dumps(pList, default=date_handler)
        return jsonify({'Orders': json.loads(x)})

    except Exception as e:
        print(e)
        abort(404)

# Mark an order delivered
@app.route('/Prescription/api/v1.0/orders/orderID=<int:orderID>', methods=['GET'])
def closeOrder(orderID):
        models.Order.closeOrder(orderID)
        return jsonify({'Orders': {}})



#get all orders for patient

@app.route('/Prescription/api/v1.0/orders/patient=<int:patient_id>', methods=['GET'])
def getPatientOrders(patient_id):
    try:
        orders = models.Order.getAllOrdersforPatient(patient_id)
        x = json.dumps(orders, default=date_handler)
        return jsonify({'Orders': json.loads(x)})
    except:
        e = sys.exc_info()[0]
        print e
        abort(404)


# adds a order to the table if the input is given in a json


@app.route('/Prescription/api/v1.0/orders', methods=['POST'])
def addOrder():
    # try:
    #     validate(request.json, orderSchema)
    # except:
    #     abort(400)

    try:
        x = json.dumps(request.json)
        models.Order.addOrder(x)

        data = {'message': 'You have a new order'}
        gcmTest.sendNotification(APIKey, reg_id, data)

    except Exception as e:
        print(e)
        abort(409)

    return jsonify({'orders': request.json}), 201


##########reg token#########

@app.route('/Prescription/api/v1.0/regtoken/<string:device_id>', methods=['GET'])
def getRegToken(device_id):
    try:
        regToken = models.RegistrationToken.getRegistrationToken(device_id)
        x = json.dumps(model_to_dict(regToken), default=date_handler)
        return jsonify({'RegistrationToken': json.loads(x)})
    except Exception as e:
        print(e)
        abort(404)


@app.route('/Prescription/api/v1.0/regtoken/all', methods=['GET'])
def getAlldRegToken():

    try:
        allRegToken = models.RegistrationToken.getAllRegistrationToken()
        x = json.dumps(allRegToken)
        return jsonify({'RegistrationToken': json.loads(x)})

    except Exception as e:
        print(e)
        abort(404)


# add reg token for a device

@app.route('/Prescription/api/v1.0/regtoken', methods=['POST'])
def addRegToken():
    try:
        validate(request.json, tokenSchema)
    except:
        abort(400)

    try:
        x = json.dumps(request.json)
        models.RegistrationToken.addRegToken(x)
    except Exception as e:
        print(e)
        abort(409)

    return jsonify({'RegistrationToken': request.json}), 201

@app.route('/Prescription/api/v1.0/tokensignin', methods=['POST'])
def addSignInToken():

    try:
        x = json.dumps(request.json)
        print request.json["idToken"]
        idinfo = client.verify_id_token(request.json['idToken'], WEB_CLIENT_ID)

        if idinfo['aud'] not in [ANDROID_CLIENT_ID, WEB_CLIENT_ID]:
            raise crypt.AppIdentityError("Unrecognized client.")
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")

        res = models.Patient.addPatient(idinfo)
	y = json.dumps(model_to_dict(res), default=date_handler)

    except crypt.AppIdentityError:
        abort(400)

    return jsonify(json.loads(y)), 201

@app.route('/Prescription/api/v1.0/chemist/tokensignin', methods=['POST'])
def addChemSignInToken():

    try:
        x = json.dumps(request.json)
        print request.json["idToken"]
        token = request.json["idToken"]
        idinfo = googleTokenValidation(token, WEB_CLIENT_ID, ANDROID_CLIENT_ID)
        res = models.Chemist.addChemist(idinfo)
        y = json.dumps(model_to_dict(res), default=date_handler)

    except crypt.AppIdentityError:
        abort(400)

    return jsonify(json.loads("{}")), 201


if __name__ == '__main__':
    models.initialize()
    app.run(host='0.0.0.0')
    # app.run(debug=True)
