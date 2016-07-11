import datetime
import json

from playhouse.shortcuts import *

mysql_db = MySQLDatabase('Prescription', user='root')


def get_pretty_print(json_object):
    return json.dumps(json_object, sort_keys=True, indent=4, separators=(',', ': '))


class MySQLModel(Model):
    """A base model that will use our MySQL database"""

    class Meta:
        database = mysql_db


class Doctor(MySQLModel):
    doctor_id = PrimaryKeyField()
    first_name = CharField(null=False, max_length=100)
    last_name = CharField(null=False, max_length=100)
    phone_number = CharField(null=False, unique=True, max_length=10)
    timestamp = DateTimeField(default=datetime.datetime.now)

    @classmethod
    def addDoctor(cls, docDict):
        with mysql_db.transaction():
            Doctor.create(**docDict)

    @classmethod
    def getDoctor(cls, id):
        x = Doctor.get(Doctor.doctor_id == id)
        # x.timestamp = str(x.timestamp)
        return x

    @classmethod
    def getAllDoctor(cls):
        res = Doctor.select()
        # for row in res:
        #    row.timestamp = str(row.timestamp)
        return res


class Patient(MySQLModel):
    patient_id = PrimaryKeyField()
    first_name = CharField(default = None, max_length=100, null = True)
    last_name = CharField(default = None,max_length=100, null = True)
    phone_number = CharField(default = None,unique=True, max_length=10, null = True)
    address = CharField(max_length=200, null = True)
    blood_group = CharField(max_length=5, null = True)
    timestamp = DateTimeField(default=datetime.datetime.now)
    google_id = CharField(default = None, max_length=100, null = True)
    email = CharField(default = None, max_length=100, null = True)

    # @classmethod
    # def addPatient(cls, docDict):
    #     with mysql_db.transaction():
    #         Patient.create(**docDict)

    @classmethod
    def addPatient(cls, authData):

        first_name = authData['given_name']
        last_name = authData['family_name']
        email = authData['email']
        google_id = authData['sub']

        query = Patient.select().where(Patient.google_id == google_id)

        if not query.exists():
            patient = Patient(first_name = first_name, last_name = last_name, email = email, google_id = google_id)
            patient.save()

        res = Patient.get(google_id = google_id)
        print res
        return res

    @classmethod
    def getPatient(cls, id):
        x = Patient.get(Patient.patient_id == id)
        # x.timestamp = str(x.timestamp)
        return x

    @classmethod
    def getAllPatient(cls):
        res = Patient.select()
        # for row in res:
        #    row.timestamp = str(row.timestamp)
        return res

    @classmethod
    def getPatientID(cls, name, phone_number):
        id = Patient.get(first_name=name, phone_number=phone_number)
        return id.patient_id

    @classmethod
    def addInfo(cls, request, patientID):

        try:
            phone = request['phone']
            address = request['address']
            bloodGrp = request['blood_grp']

            print phone, address, bloodGrp

            Patient.update(phone_number = phone, address = address, blood_group = bloodGrp).where(Patient.patient_id == patientID).execute()
        except Exception as e:
            print(e)


class Chemist(MySQLModel):
    chemist_id = PrimaryKeyField()
    pharmacy_name = CharField(null=False, max_length=100)
    first_name = CharField(null=False, max_length=100)
    last_name = CharField(null=False, max_length=100)
    phone_number = CharField(null=False, unique=True, max_length=10)
    address = CharField(null=False, max_length=200)
    google_id = CharField(default = None, max_length=100, null = True)
    email = CharField(default = None, max_length=100, null = True)
    lat = DecimalField(max_digits=10, decimal_places=6)
    long = DecimalField(max_digits=10, decimal_places=6)
    timestamp = DateTimeField(default=datetime.datetime.now)

    # @classmethod
    # def addChemist(cls, docDict):
    #     with mysql_db.transaction():
    #         Chemist.create(**docDict)

    @classmethod
    def addChemist(cls, authData):

        first_name = authData['given_name']
        last_name = authData['family_name']
        email = authData['email']
        google_id = authData['sub']

        query = Chemist.select().where(Chemist.google_id == google_id)

        if not query.exists():
            chemist = Chemist(first_name = first_name, last_name = last_name, email = email, google_id = google_id)
            Chemist.save()

        res = Chemist.get(google_id = google_id)
        print res
        return res

    @classmethod
    def getChemist(cls, id):
        x = Chemist.get(Chemist.chemist_id == id)
        # x.timestamp = str(x.timestamp)
        return x

    @classmethod
    def getAllChemist(cls):
        res = Chemist.select()
        # for row in res:
        #    row.timestamp = str(row.timestamp)
        return res

    @classmethod
    def getChemistID(cls, name, phone_number):
        id = Chemist.get(first_name=name, phone_number=phone_number)
        return id.chemist_id



class Medicines(MySQLModel):
    medicine_id = PrimaryKeyField()
    name = CharField(null=False, max_length=256)
    default_morning = BooleanField(default=False)
    default_evening = BooleanField(default=False)
    default_night = BooleanField(default=False)

    @classmethod
    def addMedicine(self, name):
        with mysql_db.transaction():
            Medicines.create(name=name)

    @classmethod
    def getMedicine(self, name):
        Medicines.get(name=name)


class Prescription(MySQLModel):
    id = PrimaryKeyField()
    patient_id = ForeignKeyField(Patient, to_field="patient_id")
    prescription = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    @classmethod
    def addPrescription(cls, patientID, prescriptionJSON):
        with mysql_db.transaction():
            Prescription.create(patient_id=patientID, prescription=prescriptionJSON)

    @classmethod
    def getEveryPrescription(cls, id):
        l = []

        allPrescriptions = Prescription.select().where(Prescription.patient_id == id).order_by(Prescription.timestamp.desc())
        for prescription in allPrescriptions:
            l.append(model_to_dict(prescription))
        listOfPrescriptionDict = l
        return listOfPrescriptionDict

    @classmethod
    def getLatestPrescription(cls, id):
        query = "SELECT max(id) FROM Prescription.prescription where patient_id_id = %s"
        cursor = mysql_db.execute_sql(query, str(id))
        latest_id = cursor.fetchall()[0][0]

        latest_prescription_row = Prescription.get(Prescription.id == latest_id)
        return model_to_dict(latest_prescription_row)

class Order(MySQLModel):
    id = PrimaryKeyField()
    patient_id = ForeignKeyField(Patient, to_field="patient_id")
    chemist_id = ForeignKeyField(Chemist, to_field="chemist_id")
    order = TextField()
    delivered = BooleanField(default=False)
    timestamp = DateTimeField(default=datetime.datetime.now)

    @classmethod
    def addOrder(cls, orderDict):
        x = json.loads(orderDict)
        chemistid = x["chemist_id"]
        patientid = x["patient_id"]
        medJSON = x["order"]

        # print chemistid, patientid, medJSON

        with mysql_db.transaction():
            Order.create(chemist_id = chemistid, patient_id = patientid, order = json.dumps(medJSON))


    @classmethod
    def getAllOrdersforPatient(cls, id):
        l = []

        allOrders = Order.select().where(Order.patient_id == id).order_by(Order.timestamp.desc())
        for order in allOrders:
            l.append(model_to_dict(order))
        listOfOrderDict = l
        return listOfOrderDict

    @classmethod
    def getAllOpenOrdersforChemist(cls, id):
        l = []

        allOrders = Order.select().where(Order.chemist_id == id and Order.delivered == False).order_by(Order.timestamp.desc())
        for order in allOrders:
            l.append(model_to_dict(order))
        listOfOrderDict = l
        return listOfOrderDict

    @classmethod
    def getAllClosedOrdersforChemist(cls, id):
        l = []

        allOrders = Order.select().where(Order.chemist_id == id and Order.delivered == True).order_by(Order.timestamp.desc())
        for order in allOrders:
            l.append(model_to_dict(order))
        listOfOrderDict = l
        return listOfOrderDict

    @classmethod
    def getAllOrders(cls):
        res = Order.select()
        return res

    @classmethod
    def closeOrder(cls, orderID):
        Order.update(delivered = True).\
                    where(Order.id == orderID).execute()


class RegistrationToken(MySQLModel):
    id = PrimaryKeyField()
    device_id = TextField()
    registrationToken = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)



    @classmethod
    def addRegToken(cls, requestJson):

        requestJson = json.loads(requestJson)

        dev_id = str(requestJson["device_id"])
        regToken = requestJson["registrationToken"]

        # print dev_id, regToken

        query = RegistrationToken.select().where(RegistrationToken.device_id == dev_id)

        if not query.exists():
            with mysql_db.transaction():
                RegistrationToken.create(device_id = dev_id, registrationToken = regToken)
        else:
            with mysql_db.transaction():
                RegistrationToken.update(registrationToken = regToken).\
                    where(RegistrationToken.device_id == dev_id).execute()


    @classmethod
    def getRegistrationToken(cls, dev_id):

        allOrders = RegistrationToken.get(RegistrationToken.device_id == "123")
        return allOrders

    @classmethod
    def getAllRegistrationToken(cls):

        allRegToken = []
        for user in RegistrationToken.select():
            allRegToken.append(user.registrationToken)
        return allRegToken


def process(i):
    pdetails = {}

    pdetails["phone"] = i['patient_id']['phone_number']
    pdetails["first_name"] = i['patient_id']['first_name']
    pdetails["last_name"] = i['patient_id']['last_name']
    pdetails["address"] = i['patient_id']['address']
    pdetails["time"] = i['timestamp']

    pdetails["order"] = i['order']

    return pdetails

# Order.closeOrder(1)
# Order.closeOrder(2)
# Order.closeOrder(3)
# a = Order.getAllOpenOrdersforChemist(1)
# for i in a:
#     print i



def initialize():
    mysql_db.connect()
    mysql_db.create_tables([Doctor, Patient, Prescription, Chemist, Order, RegistrationToken], safe=True)
    mysql_db.close()

